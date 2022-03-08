from django.db import models
from django.utils.timezone import now


import usuarios

# Create your models here.



class TiposPlanta(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
  #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre

class PerfilesPlanta(models.Model):
    id=models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
    planta = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    tiposPlanta  = models.ForeignKey('planta.TiposPlanta', default=1, on_delete=models.PROTECT, null=True)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
  #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


def __str__(self):
        return self.estado


class Planta(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    TIPO_CHOICES= (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
    )
    id = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
 #   documento =  models.IntegerField()
    documento = models.CharField(unique=True, max_length=30)
    nombre = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    genero = models.CharField(max_length=1, default ='L',choices=TIPO_CHOICES,)
    direccion = models.CharField(max_length=50)
    telefono  = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to="fotos", null=True)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
  #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre
