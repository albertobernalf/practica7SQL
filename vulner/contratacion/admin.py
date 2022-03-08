from django.contrib import admin

# Register your models here.


from clinico.models import TiposExamen
from contratacion.models import  Procedimientos


@admin.register(Procedimientos)
class procedimientosAdmin(admin.ModelAdmin):

    list_display = ( "id","tiposExamen", "cups","nombre","solicitaEnfermeria")
    search_fields = ( "id","tiposExamen", "cups","nombre","solicitaEnfermeria")
    # Filtrar
    list_filter = ( "id","tiposExamen", "cups","nombre","solicitaEnfermeria")
