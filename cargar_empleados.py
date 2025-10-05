# cargar_empleados.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_asistencia.settings')
django.setup()

from app.models import Empleado, TipoAsistencia

# Crear empleados
Empleado.objects.bulk_create([
    Empleado(nombres="Ademir", apellidos="Arredondo", dni=10000001, contrato="Planilla"),
    Empleado(nombres="Alexis", apellidos="Vasquez Conchatupac", dni=10000002, contrato="Planilla"),
    Empleado(nombres="Carlos Fernando", apellidos="Lozano Roman", dni=10000003, contrato="Planilla"),
    Empleado(nombres="Carlos Gabriel", apellidos="More Miranda", dni=10000004, contrato="Planilla"),
    Empleado(nombres="Cecy Kattia", apellidos="Salcedo Arauda", dni=10000005, contrato="Planilla"),
    Empleado(nombres="Claudia", apellidos="Aguilar", dni=10000006, contrato="Planilla"),
    Empleado(nombres="Cristhoper", apellidos="Rufasto", dni=10000007, contrato="Planilla"),
    Empleado(nombres="Iris", apellidos="Oblitas La Rosa", dni=10000008, contrato="Planilla"),
    Empleado(nombres="Jean Leonardo", apellidos="Estrada Roque", dni=10000009, contrato="Planilla"),
    Empleado(nombres="Joel Edwin", apellidos="Llanos Mejico", dni=10000010, contrato="Planilla"),
    Empleado(nombres="Jordi Cesar Hernando", apellidos="Quezada Rosales", dni=10000011, contrato="Planilla"),
    Empleado(nombres="Jose Alberto", apellidos="Davila Paredes", dni=10000012, contrato="Planilla"),
    Empleado(nombres="Jose Angel", apellidos="Borda Hernandez", dni=10000013, contrato="Planilla"),
    Empleado(nombres="Jose Lino", apellidos="Solano Caqui", dni=10000014, contrato="Planilla"),
    Empleado(nombres="Jose Luis", apellidos="Gonzalez Romero", dni=10000015, contrato="Planilla"),
    Empleado(nombres="Julio Daniel", apellidos="Peñaherrera Orrillo", dni=10000016, contrato="Planilla"),
    Empleado(nombres="Kevin", apellidos="Paul Sanchez", dni=10000017, contrato="Planilla"),
    Empleado(nombres="Marco Antonio Jose", apellidos="Garcia Galvan", dni=10000018, contrato="Planilla"),
    Empleado(nombres="Pedro Luis", apellidos="Hernandez Reyes", dni=10000019, contrato="Planilla"),
    Empleado(nombres="Romulo", apellidos="Prieto", dni=10000020, contrato="Planilla"),
    Empleado(nombres="Ruben Dario", apellidos="Canicani Cahuana", dni=10000021, contrato="Planilla"),
    Empleado(nombres="Saul", apellidos="Gamara Quispe", dni=10000022, contrato="Planilla"),
    Empleado(nombres="Stalin", apellidos="Llulluy Ramon", dni=10000023, contrato="Planilla"),
    Empleado(nombres="Valery", apellidos="Celestino Begar", dni=10000024, contrato="Planilla"),
    Empleado(nombres="Willy Jhon", apellidos="Paco Deza", dni=10000025, contrato="Planilla"),
    Empleado(nombres="Wilmer", apellidos="Quispe Huaringa", dni=10000026, contrato="Planilla"),
    Empleado(nombres="Yuli", apellidos="Tarazona", dni=10000027, contrato="Planilla"),
    Empleado(nombres="Zhihua Santiago", apellidos="Yong Sanchez", dni=10000028, contrato="Planilla"),
    Empleado(nombres="Jaime Franksue", apellidos="Sullon Li", dni=10000029, contrato="Planilla"),
])

# Crear tipos de asistencia si no existen
tipos = [
    'Entrada', 'Salida', 'Inicio Almuerzo', 'Fin Almuerzo',
    'Entrada por comisión', 'Salida por comisión',
    'Entrada por otros', 'Salida por otros'
]
for nombre in tipos:
    TipoAsistencia.objects.get_or_create(nombre_asistencia=nombre)

print("Datos insertados correctamente.")
