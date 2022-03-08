from django.contrib import admin

# Register your models here.

from planta.models import TiposPlanta, Planta, PerfilesPlanta


@admin.register(TiposPlanta)
class tiposPlantaAdmin(admin.ModelAdmin):

    list_display=("id","nombre")
    search_fields =("id","nombre")
    #readonly_fields = ["nombre"]
    # Filtrar
    list_filter = ('nombre', )

@admin.register(PerfilesPlanta)
class perfilesPlantaAdmin(admin.ModelAdmin):

        list_display = ("id", "sedesClinica",  "tiposPlanta", "planta",)
        search_fields =  ("id", "sedesClinica",  "tiposPlanta", "planta",)
        # Filtrar
        list_filter = ('sedesClinica','planta','tiposPlanta')

@admin.register(Planta)
class plantaAdmin(admin.ModelAdmin):

    list_display = ("id","sedesClinica","tipoDoc","documento","nombre","genero","direccion","telefono")
    search_fields = ("id","sedesClinica","tipoDoc","documento","nombre","genero","direccion","telefono")
    # Filtrar
    list_filter = ('nombre','sedesClinica','documento','genero')




