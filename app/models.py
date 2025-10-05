from django.db import models

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    dni = models.IntegerField(unique=True)
    contrato = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class TipoAsistencia(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre_asistencia = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre_asistencia

class RegistroAsistencia(models.Model):
    id_registro = models.AutoField(primary_key=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoAsistencia, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    hora_registro = models.TimeField()
    descripcion = models.CharField(max_length=50, blank=True, null=True)   
    fingerprint = models.CharField(max_length=100, blank=True, null=True) # FingerprintJS ID del dispositivo

    def __str__(self):
        return f"{self.empleado} - {self.tipo.nombre_asistencia} - {self.fecha_registro} {self.hora_registro}"
