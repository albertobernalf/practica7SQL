from django.contrib import admin

# Register your models here.


from admisiones.models import Ingresos



class ingresosAdmin(admin.ModelAdmin):

    list_display=("id","sedesClinica","tipoDoc","documento","consec","fechaIngreso","fechaSalida","dependenciasActual","salidaClinica","especialidadesMedicosActual")
    search_fields =("id","sedesClinica","tipoDoc","documento","consec","fechaIngreso","fechaSalida","dependenciasActual","salidaClinica","especialidadesMedicosActual")




admin.site.register(Ingresos, ingresosAdmin)