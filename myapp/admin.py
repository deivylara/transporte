from django.contrib import admin
from  .models import Project, Licencia

@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    list_display = ('numero_licencia', 'nombre', 'dni', 'tipo_licencia', 'fecha_emision', 'fecha_expiracion')
    search_fields = ('numero_licencia', 'nombre', 'dni')
    list_filter = ('tipo_licencia', 'fecha_expiracion')

    
admin.site.register(Project)

