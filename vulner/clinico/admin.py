from django.contrib import admin

# Register your models here.

from clinico.models import Medicos, Especialidades , TiposExamen, Examenes, Historia, HistoriaExamenes, HistoriaResultados, EspecialidadesMedicos, Servicios, Diagnosticos, EstadosSalida,   EstadoExamenes,  Enfermedades, TiposFolio, TiposAntecedente, Antecedentes ,  CausasExterna, Vias , TiposIncapacidad, HistoriaExamenesCabezote, HistorialAntecedentes, TiposDiagnostico, HistorialDiagnosticos, Interconsultas, EstadosInterconsulta, HistorialDiagnosticosCabezote

@admin.register(Servicios)
class serviciosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)


@admin.register(Especialidades)
class especialidadesAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)

@admin.register(EspecialidadesMedicos)
class especialidadesMedicosAdmin(admin.ModelAdmin):
    list_display = ("id", "especialidades", "planta", "nombre")
    search_fields = ("id", "especialidades", "planta", "nombre")
    # Filtrar
    list_filter = ( "especialidades", "planta", "nombre")


@admin.register(EstadoExamenes)
class estadoExamenesAdmin(admin.ModelAdmin):

        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)


@admin.register(Enfermedades)
class enfermedadesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")
    # Filtrar
    list_filter = ('nombre',)




@admin.register(TiposExamen)
class tiposExamenAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)


@admin.register(TiposFolio)
class tiposFolioAdmin(admin.ModelAdmin):
        list_display = ("id", "nombre")
        search_fields = ("id", "nombre")
        # Filtrar
        list_filter = ('nombre',)

@admin.register(TiposAntecedente)
class tiposAntecedenteAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)


@admin.register(Antecedentes)
class antecedenteAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre","tiposAntecedente")
            search_fields = ("id", "nombre","tiposAntecedente")
            # Filtrar
            list_filter = ('nombre','tiposAntecedente')

@admin.register(CausasExterna)
class causasExternaAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)

@admin.register(Vias)
class viasAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)

@admin.register(TiposIncapacidad)
class tiposIncapacidadAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)

@admin.register(Examenes)
class examenesAdmin(admin.ModelAdmin):

    list_display = ("id","nombre","TiposExamen","codigo")
    search_fields = ("id","nombre","TiposExamen" ,"codigo")
    # Filtrar
    list_filter = ('nombre','TiposExamen','codigo')



@admin.register(HistoriaExamenes)
class historiaExamenesAdmin(admin.ModelAdmin):

    list_display = ( "id", "procedimientos", "cantidad","estadoExamenes")
    search_fields = ( "id", "procedimientos","cantidad","estadoExamenes")
    # Filtrar
    list_filter = ( "id", "procedimientos","cantidad","estadoExamenes")


@admin.register(HistorialDiagnosticosCabezote)
class historialDiagnosticosCabezoteAdmin(admin.ModelAdmin):
        list_display = ("id", "tipoDoc", "documento","folio","observaciones")
        search_fields =  ("id", "tipoDoc", "documento","folio","observaciones")
        # Filtrar
        list_filter =  ("id", "tipoDoc", "documento","folio","observaciones")



@admin.register(HistorialDiagnosticos)
class historialDiagnosticosAdmin(admin.ModelAdmin):
        list_display = ("id", "diagnosticos","tiposDiagnostico")
        search_fields = ("id", "diagnosticos","tiposDiagnostico")
        # Filtrar
        list_filter = ("id", "diagnosticos","tiposDiagnostico")


@admin.register(HistoriaExamenesCabezote)
class historiaExamenesCabezoteAdmin(admin.ModelAdmin):

    list_display = ( "id", "historia", "tiposExamen","observaciones")
    search_fields =( "id", "historia","tiposExamen","observaciones")
    # Filtrar
    list_filter = ( "id", "historia", "tiposExamen","observaciones")



@admin.register(Historia)
class historiaAdmin(admin.ModelAdmin):

        list_display = ("id", "tipoDoc", "documento","folio","fecha","causasExterna","dependenciasRealizado")
        search_fields = ("id", "tipoDoc", "documento","folio","fecha","causasExterna","dependenciasRealizado")
        # Filtrar
        list_filter = ('id', 'tipoDoc', 'documento', 'folio', 'fecha', 'causasExterna','dependenciasRealizado')


@admin.register(HistoriaResultados)
class historiaResultadosAdmin(admin.ModelAdmin):
    list_display = ("id", "tipoDoc", "documento", "folio", "fecha", "consecResultados","tiposExamen", "examen","resultado")
    search_fields =  ("id", "tipoDoc", "documento", "folio", "fecha", "consecResultados","tiposExamen", "examen","resultado")
    # Filtrar
    list_filter = ('id', 'tipoDoc', 'documento', 'folio', 'fecha', 'tiposExamen', 'examen', 'resultado', 'interpretacion')


@admin.register(TiposDiagnostico)
class tiposDiagnosticoAdmin(admin.ModelAdmin):
            list_display = ("id", "nombre")
            search_fields = ("id", "nombre")
            # Filtrar
            list_filter = ('nombre',)



@admin.register(Diagnosticos)
class diagnosticosAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ('id', 'nombre',)

@admin.register(EstadosSalida)
class estadosSalidaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")

    # Filtrar
    list_filter = ('id', 'nombre',)


@admin.register(HistorialAntecedentes)
class historialAntecedentesAdmin(admin.ModelAdmin):

        list_display = ("id", "tipoDoc", "documento","folio","tiposAntecedente","antecedentes","descripcion")
        search_fields = ("id", "tipoDoc", "documento","folio","tiposAntecedente","antecedentes","descripcion")
        # Filtrar
        list_filter = ("id", "tipoDoc", "documento","folio","tiposAntecedente","antecedentes","descripcion")



@admin.register(EstadosInterconsulta)
class estadosInterconsultaAdmin(admin.ModelAdmin):
     list_display = ("id", "nombre")
     search_fields = ("id", "nombre")
      # Filtrar
     list_filter = ('id', 'nombre',)


@admin.register(Interconsultas)
class interconsultasdmin(admin.ModelAdmin):

        list_display = ("id", "tipoDoc", "documento","folio","descripcionConsulta","especialidadConsultada","respuestaConsulta")
        search_fields = ("id", "tipoDoc", "documento","folio","descripcionConsulta","especialidadConsultada","respuestaConsulta")
        # Filtrar
        list_filter =("id", "tipoDoc", "documento","folio","descripcionConsulta","especialidadConsultada","respuestaConsulta")
