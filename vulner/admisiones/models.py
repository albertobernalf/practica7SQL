from django.db import models
from django.utils.timezone import now

# Create your models here.

class Ingresos(models.Model):

    id           = models.AutoField(primary_key=True)
    sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True, related_name = 'SedesClinica')
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
    documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True, related_name='Documento')
    consec    = models.IntegerField()
    fechaIngreso = models.DateTimeField(default=now, editable=True)
    fechaSalida = models.DateTimeField(default=now, editable=True)
    factura  = models.IntegerField(default=0)
    numcita  =  models.IntegerField(default=0)
    #serviciosIng = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True,  related_name='id9')
    dependenciasIngreso = models.ForeignKey('sitios.Dependencias', default=1, on_delete=models.PROTECT, null=True,  related_name='id0')
    dxIngreso = models.ForeignKey('clinico.Diagnosticos', default=1, on_delete=models.PROTECT, null=True ,  related_name='id3')
    medicoIngreso  =  models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True,  related_name='id6')

    especialidadesMedicosIngreso =  models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT, null=True,  related_name='EspIng')

    #serviciosActual = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True,  related_name='id10')
    dependenciasActual = models.ForeignKey('sitios.Dependencias', default=1, on_delete=models.PROTECT, null=True,  related_name='id1')
    dxActual = models.ForeignKey('clinico.Diagnosticos', default=1, on_delete=models.PROTECT, null=True,  related_name='id4')
    medicoActual =  models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True,  related_name='id7')
    especialidadesMedicosActual = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT,
                                                     null=True, related_name='EspAct')
    estadoSalida  = models.ForeignKey('clinico.EstadosSalida', default=1, on_delete=models.PROTECT, null=True)
   # serviciosSalida  = models.ForeignKey('clinico.Servicios', default=1, on_delete=models.PROTECT, null=True,  related_name='id11')
    dependenciasSalida = models.ForeignKey('sitios.Dependencias', default=1, on_delete=models.PROTECT, null=True,  related_name='id2')
    dxSalida = models.ForeignKey('clinico.Diagnosticos', default=1, on_delete=models.PROTECT, null=True,  related_name='id5')
    medicoSalida =  models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True,  related_name='id8')
    especialidadesMedicosSalida = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT,
                                                     null=True, related_name='EspSal')
    salidaClinica = models.CharField(max_length=1,default='N')
    salidaDefinitiva =  models.CharField(max_length=1,default='N')
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)



