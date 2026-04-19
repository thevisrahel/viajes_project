from django.contrib import admin
from viajes_app.models import Viaje



class ProductoAdmin(admin. ModelAdmin):
    list_display = ['destino', 'descripcion','fecha']
    list_filter = ['destino', 'fecha']

admin.site.register(Viaje, ProductoAdmin)