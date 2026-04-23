from django.contrib import admin
from .models import Viaje


class ViajeAdmin(admin.ModelAdmin):
    list_display = ['id', 'propietario', 'region', 'sitio_turistico', 'fecha']
    list_filter = ['region', 'fecha']
    search_fields = ['region', 'sitio_turistico']


admin.site.register(Viaje, ViajeAdmin)