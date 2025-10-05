from django.shortcuts import render
from .models import Empleado, TipoAsistencia, RegistroAsistencia
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta
from collections import defaultdict
from openpyxl.styles import Font, PatternFill, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo


def es_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(es_staff)
def pagina_descarga_excel(request):
    return render(request, 'pagina_descarga_excel.html')

def strfdelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours:02d}:{minutes:02d}"

from datetime import datetime, timedelta
from collections import defaultdict

def strfdelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes = remainder // 60
    return f"{hours:02d}:{minutes:02d}"

@user_passes_test(es_staff)
def exportar_resumen_excel(request):
    from datetime import datetime, timedelta
    from collections import defaultdict

    def delta(t1, t2):
        return datetime.combine(datetime.today(), t2) - datetime.combine(datetime.today(), t1)

    def strfdelta(td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02d}:{minutes:02d}"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Resumen Diario"

    # Encabezados
    encabezados = [
        "Empleado", "Fecha", "Tiempo de Almuerzo",
        "Horas por Comisión", "Horas por Permiso (Otros)",
        "Horas Trabajadas Totales"
    ]
    ws.append(encabezados)

    registros = RegistroAsistencia.objects.select_related('empleado', 'tipo') \
        .order_by('empleado', 'fecha_registro', 'hora_registro')

    datos_diarios = defaultdict(lambda: defaultdict(list))
    for reg in registros:
        key = (reg.empleado.id_empleado, reg.fecha_registro)
        datos_diarios[key]["empleado"] = reg.empleado
        datos_diarios[key]["fecha"] = reg.fecha_registro
        datos_diarios[key][reg.tipo.nombre_asistencia].append(reg.hora_registro)

    for (id_empleado, fecha), data in datos_diarios.items():
        empleado = data["empleado"]
        almuerzo = timedelta()
        comision = timedelta()
        permiso = timedelta()
        trabajadas = timedelta()

        if "Inicio almuerzo" in data and "Fin almuerzo" in data:
            almuerzo = delta(data["Inicio almuerzo"][0], data["Fin almuerzo"][0])
        if "Salida por comisión" in data and "Entrada por comisión" in data:
            comision = delta(data["Salida por comisión"][0], data["Entrada por comisión"][0])
        if "Salida por otros" in data and "Entrada por otros" in data:
            permiso = delta(data["Salida por otros"][0], data["Entrada por otros"][0])
        if "Entrada" in data and "Salida" in data:
            total_dia = delta(data["Entrada"][0], data["Salida"][0])
            trabajadas = total_dia - almuerzo - permiso

        ws.append([
            f"{empleado.nombres} {empleado.apellidos}",
            fecha.strftime("%Y-%m-%d"),
            strfdelta(almuerzo),
            strfdelta(comision),
            strfdelta(permiso),
            strfdelta(trabajadas)
        ])

    # Ajustar ancho de columnas
    for col in ws.columns:
        max_length = max(len(str(cell.value)) for cell in col if cell.value)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    # Aplicar estilo al encabezado
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="4F81BD")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border

    # Crear tabla
    tabla = Table(
        displayName="ResumenAsistencia",
        ref=f"A1:F{ws.max_row}"
    )
    style = TableStyleInfo(
        name="TableStyleMedium9", showFirstColumn=False,
        showLastColumn=False, showRowStripes=True, showColumnStripes=False
    )
    tabla.tableStyleInfo = style
    ws.add_table(tabla)

    # Enviar archivo
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=resumen_asistencia.xlsx'
    wb.save(response)
    return response

@user_passes_test(es_staff)
def exportar_asistencia_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Asistencia"

    # Encabezados del excel
    encabezados = ["Empleado", "Tipo de Asistencia", "Fecha", "Hora", "Descripción", "ID Dispositivo"]
    ws.append(encabezados)

    # Registros
    registros = RegistroAsistencia.objects.select_related('empleado', 'tipo') \
        .order_by('-fecha_registro', '-hora_registro')
    for reg in registros:
        fila = [
            f"{reg.empleado.nombres} {reg.empleado.apellidos}",
            reg.tipo.nombre_asistencia,
            reg.fecha_registro.strftime('%Y-%m-%d'),
            reg.hora_registro.strftime('%H:%M:%S'),
            reg.descripcion or '',
            reg.fingerprint or '',
        ]
        ws.append(fila)

    # Ajustar ancho de columnas
    for col in ws.columns:
        max_length = max(len(str(cell.value)) for cell in col if cell.value)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    # Estilo encabezado
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="4F81BD")
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border

    # Tabla
    tabla = Table(
        displayName="RegistroAsistencia",
        ref=f"A1:F{ws.max_row + 1}"
    )
    style = TableStyleInfo(
        name="TableStyleMedium9", showFirstColumn=False,
        showLastColumn=False, showRowStripes=True, showColumnStripes=False
    )
    tabla.tableStyleInfo = style
    ws.add_table(tabla)

    # Respuesta
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=registro_asistencia.xlsx'
    wb.save(response)
    return response



def registrar_asistencia(request):
    empleados = Empleado.objects.all()
    tipos_evento = TipoAsistencia.objects.all()

    if request.method == 'POST':
        empleado_id = request.POST.get('empleado')
        tipo_id = int(request.POST.get('tipo_evento'))
        descripcion = request.POST.get('descripcion') or ''
        fingerprint = request.POST.get('fingerprint')

        now = timezone.localtime()
        fecha = now.date()
        hora = now.time()

        empleado = Empleado.objects.get(id_empleado=empleado_id)
        tipo_asistencia = TipoAsistencia.objects.get(id_tipo=tipo_id)

        tipos_unicos = ['Entrada', 'Inicio Almuerzo', 'Fin Almuerzo', 'Salida']

        # Validar si ese tipo ya fue registrado por este empleado hoy
        if tipo_asistencia.nombre_asistencia in tipos_unicos:
            ya_existe = RegistroAsistencia.objects.filter(
                empleado=empleado,
                tipo=tipo_asistencia,
                fecha_registro=fecha
            ).exists()
            if ya_existe:
                messages.warning(request, f'Ya registraste "{tipo_asistencia.nombre_asistencia}" hoy.')
                return render(request, 'formulario.html', {
                    'empleados': empleados,
                    'tipos_evento': tipos_evento
                })

        # Validar si este fingerprint ya fue usado hoy por otro empleado
        uso_invalido = RegistroAsistencia.objects.filter(
            ~Q(empleado=empleado),
            fingerprint=fingerprint,
            fecha_registro=fecha
        ).exists()
        if uso_invalido:
            messages.error(request, "Este dispositivo ya ha sido usado para registrar la asistencia de otro empleado hoy.")
            return render(request, 'formulario.html', {
                'empleados': empleados,
                'tipos_evento': tipos_evento
            })

        RegistroAsistencia.objects.create(
            empleado=empleado,
            tipo=tipo_asistencia,
            fecha_registro=fecha,
            hora_registro=hora,
            descripcion=descripcion,
            fingerprint=fingerprint
        )

        messages.success(request, f'{tipo_asistencia.nombre_asistencia} registrada correctamente.')
        return render(request, 'asistencia_exitosa.html', {
            'fecha': fecha,
            'hora': hora,
            'empleado': empleado
        })

    return render(request, 'formulario.html', {
        'empleados': empleados,
        'tipos_evento': tipos_evento
    })
