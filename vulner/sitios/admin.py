from django.contrib import admin

# Register your models here.

from sitios.models import Departamentos, Ciudades, Centros, SedesClinica, DependenciasTipo, Dependencias, DependenciasActual, ServiciosSedes, SubServiciosSedes, HistorialDependencias

@admin.register(SedesClinica)
class sedesClinicaAdmin(admin.ModelAdmin):


    list_display = ("id","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
    search_fields = ("id","departamentos","ciudades", "nombre","direccion", "telefono", "contacto","fechaRegistro")
    #Filtrar
    list_filter =('nombre', 'ciudades')


class CiudadesAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("id", "nombre")

    # Filtrar
    list_filter = ('nombre',)


class DepartamentosAdmin(admin.ModelAdmin):


    list_display=("id","nombre")

    search_fields =("id","nombre")
    # Filtrar
    list_filter = ('nombre',)

admin.site.register(Departamentos, DepartamentosAdmin)
admin.site.register(Ciudades, CiudadesAdmin)




@admin.register(Centros)
class centrosAdmin(admin.ModelAdmin):
        list_related_name = 'ciudadesDepartamentos'

        list_display = ("id","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
        search_fields = ("id","departamentos","ciudades" , "nombre","direccion", "telefono", "contacto","fechaRegistro")
        # Filtrar
        list_filter = ('nombre','departamentos','ciudades','contacto')



@admin.register(ServiciosSedes)
class serviciosSedesAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "servicios","nombre")
    search_fields = ("id","sedesClinica", "servicios","nombre")
    # Filtrar
    list_filter = ('nombre', "sedesClinica", "servicios",)


@admin.register(SubServiciosSedes)
class SubServiciosSedesAdmin(admin.ModelAdmin):


    list_display = ("id","sedesClinica", "servicios","nombre")
    search_fields = ("id","sedesClinica", "servicios","nombre")
    # Filtrar
    list_filter = ('nombre', "sedesClinica", "servicios",)



@admin.register(DependenciasTipo)
class dependenciasTipoAdmin(admin.ModelAdmin):


    list_display = ("id","nombre")
    search_fields = ("id","nombre")
    # Filtrar
    list_filter = ('nombre',)

@admin.register(Dependencias)
class dependenciasAdmin(admin.ModelAdmin):


    list_display = ("id", "sedesClinica","servicios","subServicios","numero", "dependenciasTipo", "nombre", "descripcion")
    search_fields =  ("id", "sedesClinica","servicios","subServicios", "numero", "dependenciasTipo", "nombre", "descripcion")
    fields =  ("sedesClinica","servicios","subServicios", "dependenciasTipo","numero", "nombre", "descripcion")
    # Filtrar
    list_filter = ('nombre', "sedesClinica","servicios","subServicios","numero", 'dependenciasTipo','descripcion')


@admin.register(DependenciasActual)
class dependenciasActualAdmin(admin.ModelAdmin):


    list_display = ("id","dependencias", "tipoDoc", "documento","consec","fecha", "disponibilidad", "fechaRegistro")
    search_fields = ("id","dependencias", "tipoDoc", "documento","consec","fecha", "disponibilidad", "fechaRegistro")


@admin.register(HistorialDependencias)
class historialDependenciasAdmin(admin.ModelAdmin):


    list_display = ("id","dependencias", "tipoDoc", "documento","consec","fechaOcupacion", "fechaLiberacion", "fechaRegistro")
    fields = ( "dependencias", "tipoDoc", "documento", "consec", "fechaOcupacion", "fechaLiberacion", "fechaRegistro")
    search_fields = ("id","dependencias", "tipoDoc", "documento","consec","fechaOcupacion", "fechaLiberacion", "fechaRegistro")

admin.site.site_header = 'Clinica Vulnerable'
admin.site.index_title = 'Panel de control '
admin.site.site_title = 'Administracion'



