from django.db import models
from django.utils.timezone import now

from smart_selects.db_fields import ChainedForeignKey
from sitios.models import Departamentos, Ciudades


# Create your models here.


class TiposDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    abreviatura= models.CharField(max_length=2)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
   # usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


    def __str__(self):
        return self.nombre

class TiposUsuario(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
 #   usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)


    def __str__(self):
        return self.nombre

class Usuarios(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    TIPO_CHOICES= (
        (MASCULINO, 'Masculino'),
        (FEMENINO, 'Femenino'),
    )
    id = models.AutoField(primary_key=True)
    tipoDoc= models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
    #documento =  models.IntegerField(unique=True)
    documento = models.CharField(unique=True,max_length=30)
    nombre = models.CharField(max_length=50)
    genero = models.CharField(max_length=1, default ='L',choices=TIPO_CHOICES,)
    centrosC = models.ForeignKey('sitios.Centros', default=1, on_delete=models.PROTECT, null=True)
    tiposUsuario = models.ForeignKey('usuarios.TiposUsuario', default=1, on_delete=models.PROTECT, null=True)
    fechaNacio = models.DateTimeField(default=now, editable=False)
    departamentos = models.ForeignKey('sitios.Departamentos', default=1, on_delete=models.PROTECT, null=True)

    ciudades = ChainedForeignKey(Ciudades, chained_field='departamentos', chained_model_field='departamentosUsuarios',  show_all=False)
    direccion = models.CharField(max_length=50)
    telefono  = models.CharField(max_length=20)
    contacto  = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="fotos", null=True)

    fechaRegistro = models.DateTimeField(default=now, editable=False)
   # usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


