from django.db import models
from django.utils.timezone import now

# Create your models here.


class Procedimientos(models.Model):
    Si = 'S'
    No = 'N'
    TIPO_CHOICES = (
        (Si, 'Si'),
        (No, 'No'),
    )
    id = models.AutoField(primary_key=True)
    tiposExamen = models.ForeignKey('clinico.TiposExamen',on_delete=models.PROTECT, null= False)
    cups = models.CharField(max_length=20, null=False, default=0)
    nombre = models.CharField(max_length=80)
    solicitaEnfermeria = models.CharField(max_length=1 ,choices=TIPO_CHOICES,)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
            return self.nombre


