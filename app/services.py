"""
Servicios de negocio para el sistema de asistencia.
Contiene la lógica de negocio separada de las vistas.
"""

from datetime import datetime, timedelta
from collections import defaultdict
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .models import Empleado, TipoAsistencia, RegistroAsistencia


class AsistenciaService:
    """Servicio para manejar la lógica de negocio de asistencia."""
    
    TIPOS_UNICOS = ['Entrada', 'Inicio Almuerzo', 'Fin Almuerzo', 'Salida']
    
    @staticmethod
    def validar_registro_duplicado(empleado, tipo_asistencia, fecha):
        """
        Valida si ya existe un registro del mismo tipo para el empleado en la fecha.
        
        Args:
            empleado: Instancia de Empleado
            tipo_asistencia: Instancia de TipoAsistencia
            fecha: Fecha a validar
            
        Returns:
            bool: True si ya existe el registro
        """
        if tipo_asistencia.nombre_asistencia in AsistenciaService.TIPOS_UNICOS:
            return RegistroAsistencia.objects.filter(
                empleado=empleado,
                tipo=tipo_asistencia,
                fecha_registro=fecha
            ).exists()
        return False
    
    @staticmethod
    def validar_fingerprint_unico(empleado, fingerprint, fecha):
        """
        Valida que el fingerprint no haya sido usado por otro empleado en la fecha.
        Si no se proporciona fingerprint (None o cadena vacía), no aplica la validación.
        
        Args:
            empleado: Instancia de Empleado
            fingerprint: ID del dispositivo
            fecha: Fecha a validar
            
        Returns:
            bool: True si el fingerprint ya fue usado por otro empleado
        """
        # Si no hay fingerprint, no bloquear el registro (flujo sin identificación de dispositivo)
        if not fingerprint:
            return False
        return RegistroAsistencia.objects.filter(
            ~Q(empleado=empleado),
            fingerprint=fingerprint,
            fecha_registro=fecha
        ).exists()
    
    @staticmethod
    def crear_registro_asistencia(empleado_id, tipo_id, descripcion, fingerprint):
        """
        Crea un nuevo registro de asistencia.
        
        Args:
            empleado_id: ID del empleado
            tipo_id: ID del tipo de asistencia
            descripcion: Descripción adicional
            fingerprint: ID del dispositivo
            
        Returns:
            tuple: (success, message, registro)
        """
        try:
            empleado = Empleado.objects.get(id_empleado=empleado_id)
            tipo_asistencia = TipoAsistencia.objects.get(id_tipo=tipo_id)
            
            now = timezone.localtime()
            fecha = now.date()
            hora = now.time()
            
            # Validar registro duplicado
            if AsistenciaService.validar_registro_duplicado(empleado, tipo_asistencia, fecha):
                return False, f'Ya registraste "{tipo_asistencia.nombre_asistencia}" hoy.', None
            
            # Validar fingerprint único
            if AsistenciaService.validar_fingerprint_unico(empleado, fingerprint, fecha):
                return False, "Este dispositivo ya ha sido usado para registrar la asistencia de otro empleado hoy.", None
            
            # Crear registro
            registro = RegistroAsistencia.objects.create(
                empleado=empleado,
                tipo=tipo_asistencia,
                fecha_registro=fecha,
                hora_registro=hora,
                descripcion=descripcion,
                fingerprint=fingerprint
            )
            
            return True, f'{tipo_asistencia.nombre_asistencia} registrada correctamente.', registro
            
        except (Empleado.DoesNotExist, TipoAsistencia.DoesNotExist):
            return False, "Error: Empleado o tipo de asistencia no encontrado.", None
        except Exception as e:
            return False, f"Error inesperado: {str(e)}", None


class ReporteService:
    """Servicio para generar reportes de asistencia."""
    
    @staticmethod
    def strfdelta(td):
        """
        Convierte un timedelta a formato HH:MM.
        
        Args:
            td: timedelta object
            
        Returns:
            str: Formato HH:MM
        """
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02d}:{minutes:02d}"
    
    @staticmethod
    def delta(t1, t2):
        """Calcula la diferencia entre dos horas del mismo día."""
        return datetime.combine(datetime.today(), t2) - datetime.combine(datetime.today(), t1)
    
    @staticmethod
    def obtener_datos_resumen():
        """
        Obtiene los datos para el resumen diario de asistencia.
        
        Returns:
            dict: Datos organizados por empleado y fecha
        """
        registros = RegistroAsistencia.objects.select_related('empleado', 'tipo') \
            .order_by('empleado', 'fecha_registro', 'hora_registro')
        
        datos_diarios = defaultdict(lambda: defaultdict(list))
        for reg in registros:
            key = (reg.empleado.id_empleado, reg.fecha_registro)
            datos_diarios[key]["empleado"] = reg.empleado
            datos_diarios[key]["fecha"] = reg.fecha_registro
            datos_diarios[key][reg.tipo.nombre_asistencia].append(reg.hora_registro)
        
        return datos_diarios
    
    @staticmethod
    def calcular_horas_empleado(data):
        """
        Calcula las horas trabajadas, almuerzo, comisiones y permisos para un empleado.
        Hace las búsquedas de tipos de asistencia de forma case-insensitive para evitar errores por variaciones de mayúsculas/minúsculas.
        
        Args:
            data: Datos del empleado para una fecha específica
            
        Returns:
            dict: Horas calculadas
        """
        almuerzo = timedelta()
        comision = timedelta()
        permiso = timedelta()
        trabajadas = timedelta()

        def get_times(key: str):
            k = key.lower()
            for existente, tiempos in data.items():
                if str(existente).lower() == k:
                    return tiempos
            return []

        ini_almuerzo = get_times("Inicio Almuerzo")
        fin_almuerzo = get_times("Fin Almuerzo")
        sal_comision = get_times("Salida por comisión")
        ent_comision = get_times("Entrada por comisión")
        sal_otros = get_times("Salida por otros")
        ent_otros = get_times("Entrada por otros")
        entrada = get_times("Entrada")
        salida = get_times("Salida")

        if ini_almuerzo and fin_almuerzo:
            almuerzo = ReporteService.delta(ini_almuerzo[0], fin_almuerzo[0])
        if sal_comision and ent_comision:
            comision = ReporteService.delta(sal_comision[0], ent_comision[0])
        if sal_otros and ent_otros:
            permiso = ReporteService.delta(sal_otros[0], ent_otros[0])
        if entrada and salida:
            total_dia = ReporteService.delta(entrada[0], salida[0])
            trabajadas = total_dia - almuerzo - permiso
        
        return {
            'almuerzo': ReporteService.strfdelta(almuerzo),
            'comision': ReporteService.strfdelta(comision),
            'permiso': ReporteService.strfdelta(permiso),
            'trabajadas': ReporteService.strfdelta(trabajadas)
        }
