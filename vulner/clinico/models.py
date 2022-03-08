from django.db import models
from django.utils.timezone import now

# Create your models here.



class Servicios(models.Model):
    id = models.AutoField(primary_key=True)
    #sedesClinica = models.ForeignKey('sitios.SedesClinica', default=1, on_delete=models.PROTECT, null=True)
    nombre = models.CharField(max_length=30, null = False)


    def __str__(self):
        return self.nombre

class EspecialidadesMedicos(models.Model):
    id = models.AutoField(primary_key=True)
    especialidades = models.ForeignKey('clinico.Especialidades', on_delete=models.PROTECT, null=False,related_name ='especialidadesMedicos1')
    planta = models.ForeignKey('planta.Planta', on_delete = models.PROTECT, null = False)
    nombre = models.CharField(max_length=30, default="" , null = False)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=False ,related_name ='usuarioRegistroPlanta')
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __integer__(self):
        return self.nombre


class Especialidades(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30 , null = False)

    def __str__(self):
        return self.nombre

class Medicos(models.Model):
        id = models.AutoField(primary_key=True)
        id_tipo_doc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=True)
        documento = models.IntegerField(default=1)
        nombre = models.CharField(max_length=30)
        id_especialidad = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT, null=True)
        id_departamento = models.ForeignKey('sitios.Departamentos', default=1, on_delete=models.PROTECT, null=True)
        id_ciudad = models.ForeignKey('sitios.Ciudades', default=1, on_delete=models.PROTECT, null=True)
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=20)
        contacto = models.CharField(max_length=50)
        id_centro = models.ForeignKey('sitios.Centros', default=1, on_delete=models.PROTECT, null=True)
        estado = models.CharField(max_length=1)

        def __str__(self):
            return self.nombre



class EstadoExamenes(models.Model):
      id = models.AutoField(primary_key=True)
      nombre = models.CharField(max_length=30, null=False)
      estadoReg = models.CharField(max_length=1, default='A', editable=False)

      def __str__(self):
          return self.nombre


class Enfermedades(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre



class TiposExamen(models.Model):
            id = models.AutoField(primary_key=True)
            nombre = models.CharField(max_length=30, null=False)
            estadoReg = models.CharField(max_length=1, default='A', editable=False)

            def __str__(self):
                return self.nombre


class TiposFolio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


class TiposAntecedente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


class Antecedentes(models.Model):
    id = models.AutoField(primary_key=True)
    tiposAntecedente = models.ForeignKey('clinico.TiposAntecedente', default=1, on_delete=models.PROTECT, null=False)
    nombre = models.CharField(max_length=50, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


class CausasExterna(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre

class Vias(models.Model):
        id = models.AutoField(primary_key=True)
        nombre = models.CharField(max_length=50, null=False)
        estadoReg = models.CharField(max_length=1, default='A', editable=False)

        def __str__(self):
            return self.nombre


class TiposIncapacidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre




class Examenes(models.Model):
                id = models.AutoField(primary_key=True)
                TiposExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT, null=False)
                codigo = models.CharField(max_length=20, null=False, default=0)
                nombre = models.CharField(max_length=80)

                def __str__(self):
                    return self.nombre

class EstadosInterconsulta(models.Model):
                id = models.AutoField(primary_key=True)
                nombre = models.CharField(max_length=30, null=False)
                estadoReg = models.CharField(max_length=1, default='A', editable=False)

                def __str__(self):
                    return self.nombre



class Interconsultas(models.Model):

                id  = models.AutoField(primary_key=True)
                tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=False)
                documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False,
                                              related_name='DocumentoHistoriaInterconsulta')
                consecAdmision = models.IntegerField(default=0)
                folio = models.IntegerField(default=0)
                descripcionConsulta = models.CharField(max_length=200)
                especialidadConsultada = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT, null=False)
                plantaConsultado  = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=True)
                respuestaConsulta = models.CharField(max_length=200)
                diagnosticos = models.ForeignKey('clinico.Diagnosticos', default=1, on_delete=models.PROTECT, null=True)
                estadosInterconsulta = models.ForeignKey('clinico.EstadosInterconsulta', default=1, on_delete=models.PROTECT, null=True)
                estadoReg = models.CharField(max_length=1, default='A', editable=False)

                def __str__(self):
                    return self.descripcionConsulta

class Historia(models.Model):
                id = models.AutoField(primary_key=True)
                tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=False)
                documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False,
                                              related_name='DocumentoHistoria')
                consecAdmision = models.IntegerField(default=0)
                folio =  models.IntegerField(default=0)
                fecha = models.DateTimeField()
                tiposFolio = models.ForeignKey('clinico.TiposFolio', default=1, on_delete=models.PROTECT, null=False)
                causasExterna = models.ForeignKey('clinico.causasExterna', default=1, on_delete=models.PROTECT, null=False)
                dependenciasRealizado = models.ForeignKey('sitios.Dependencias', default=1, on_delete=models.PROTECT,        null=False)
                especialidades = models.ForeignKey('clinico.Especialidades', default=1, on_delete=models.PROTECT, null=False)
                planta   = models.ForeignKey('planta.Planta', default=1, on_delete=models.PROTECT, null=False)
                motivo     = models.CharField(max_length=250,blank=True)
                subjetivo  = models.CharField(max_length=250, blank=True)
                objetivo   = models.CharField(max_length=250,blank=True)
                analisis   = models.CharField(max_length=250, blank=True)
                plan       = models.CharField(max_length=250, blank=True)
                fechaRegistro = models.DateTimeField(default=now, editable=False)
                usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
                estadoReg = models.CharField(max_length=1, default='A', editable=False)



                def __str__(self):
                    return str(self.id)

                class Meta:
                    ordering = ["tipoDoc","documento","folio","fecha","especialidades","motivo","subjetivo","objetivo","analisis","plan"]


class HistoriaExamenesCabezote(models.Model):
           id = models.AutoField(primary_key=True)
           historia = models.ForeignKey('clinico.Historia', default=1, on_delete=models.PROTECT, null=False)
          # tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=False)
           #documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False, related_name='DocumentoHistoriaExamenesCabezote')
           #consecAdmision = models.IntegerField(default=0)
           #folio = models.IntegerField()
           tiposExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT, null=False)
           observaciones = models.CharField(max_length=200,  editable=True)
         #  fechaRegistro = models.DateTimeField(default=now, editable=False)
         #  usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False)
           estadoReg = models.CharField(max_length=1, default='A', editable=False)


           def __str__(self):
                 return self.observaciones

class HistoriaExamenes(models.Model):
                id = models.AutoField(primary_key=True)
                historiaExamenesCabezote = models.ForeignKey('clinico.HistoriaExamenesCabezote', default=1, on_delete=models.PROTECT, null=False)
                procedimientos = models.ForeignKey('contratacion.Procedimientos', on_delete=models.PROTECT, null=False, default=1)
                #tiposExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT, null=False)
                #examen = models.ForeignKey('clinico.Examenes', default=1, on_delete=models.PROTECT, null=False)
                cantidad  = models.IntegerField()
                estadoExamenes = models.ForeignKey('clinico.EstadoExamenes', default=1, on_delete=models.PROTECT,  null=False)
                estadoReg = models.CharField(max_length=1, default='A', editable=False)


                def __str__(self):
                        return str(self.cantidad)

class HistoriaResultados(models.Model):
                    id = models.AutoField(primary_key=True)

                    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT,
                                                null=False)
                    documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False,
                                                  related_name='DocumentoHistoriaResul')
                    consecAdmision = models.IntegerField(default=0)
                    dependenciasRealizado = models.ForeignKey('sitios.Dependencias', default=1, on_delete=models.PROTECT, null=False)
                    folio = models.IntegerField()
                    fecha = models.DateTimeField()


                    consecResultados = models.IntegerField(default=0)
                    tiposExamen = models.ForeignKey('clinico.TiposExamen', default=1, on_delete=models.PROTECT,
                                                    null=False)
                    examen = models.ForeignKey('clinico.Examenes', default=1, on_delete=models.PROTECT, null=False)
                    cantidad = models.IntegerField()
                    resultado = models.CharField(max_length=500, default='')
                    interpretacion = models.CharField(max_length=500, default='')
                    estadoExamenes =  models.ForeignKey('clinico.EstadoExamenes', default=1, on_delete=models.PROTECT, null=False)
                    rutaArchivo =  models.CharField(max_length=100, default='')
                    rutaVideo =  models.CharField(max_length=100, default='')
                    estadoReg = models.CharField(max_length=1, default='A', editable=False)

                    def __str__(self):
                        return self.resultado



class TiposDiagnostico(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre



class Diagnosticos(models.Model):
    id = models.AutoField(primary_key=True)
    cie10  = models.CharField(max_length=15, default='')
    nombre = models.CharField(max_length=30 , null=False)
    descripcion = models.CharField(max_length=80)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    #usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.nombre


class EstadosSalida(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Incapacidades(models.Model):
    id = models.AutoField(primary_key=True)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT,   null=False)
    documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False,  related_name='DocumentoIncapacidades')
    consecAdmision = models.IntegerField()
    dependenciasRealizado = models.ForeignKey('sitios.Dependencias', default=1, on_delete=models.PROTECT, null=False)
    folio = models.IntegerField()
    fecha = models.DateTimeField()
    tiposIncapacidad =  models.ForeignKey('clinico.TiposIncapacidad', default=1, on_delete=models.PROTECT, null=False)
    desdeFecha = models.DateTimeField()
    hastaFecha = models.DateTimeField()
    diagnosticos =  models.ForeignKey('clinico.Diagnosticos', default=1, on_delete=models.PROTECT, null=False)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.documento



class HistorialDiagnosticosCabezote(models.Model):
    id = models.AutoField(primary_key=True)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT,   null=False)
    documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False,  related_name='DocumentoHistoriaDiag')
    consecAdmision = models.IntegerField()
    folio = models.IntegerField()
    observaciones = models.CharField(max_length=200)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.observaciones



class HistorialDiagnosticos(models.Model):
    id = models.AutoField(primary_key=True)
    historialDiagnosticosCabezote =  models.ForeignKey('clinico.HistorialDiagnosticosCabezote', default=1, on_delete=models.PROTECT, null=False,  related_name='DocumentoHistoriaDiag')
    diagnosticos =  models.ForeignKey('clinico.Diagnosticos', default=1, on_delete=models.PROTECT, null=False ,  related_name='dxPpal')
    tiposDiagnostico = models.ForeignKey('clinico.TiposDiagnostico', default=1, on_delete=models.PROTECT, null=False ,  related_name='tiposDiagnostico')
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.documento


class HistorialAntecedentes(models.Model):
    id = models.AutoField(primary_key=True)
    tipoDoc = models.ForeignKey('usuarios.TiposDocumento', default=1, on_delete=models.PROTECT, null=False)
    documento = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=False,     related_name='DocumentoAntecedentes')
    consecAdmision = models.IntegerField(default=0)
    folio = models.IntegerField(default=0)
    tiposAntecedente = models.ForeignKey('clinico.TiposAntecedente', on_delete=models.PROTECT, null=False)
    antecedentes  = models.ForeignKey('clinico.Antecedentes', on_delete=models.PROTECT, null=False)
    descripcion = models.CharField(max_length=200)
    fechaRegistro = models.DateTimeField(default=now, editable=False)
    usuarioRegistro = models.ForeignKey('usuarios.Usuarios', default=1, on_delete=models.PROTECT, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=False)

    def __str__(self):
        return self.descripcion