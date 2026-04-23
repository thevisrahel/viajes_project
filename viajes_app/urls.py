from django.urls import path
from . import views

app_name = 'viajes_app'

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('crear/', views.crear_viaje, name='crear_viaje'),
    path('listar/', views.listar_viajes, name='listar_viajes'),
    path('viajes/<int:id_viaje>/', views.detalle_viajes, name='detalle_viaje'),
    path('viajes/<int:id_viaje>/actualizar/', views.actualizar_viajes, name='actualizar_viaje'),
    path('viajes/<int:id_viaje>/eliminar/', views.eliminar_viajes, name='eliminar_viaje'),
    path('viaje/<int:viaje_id>/like/', views.toggle_like, name='toggle_like'),
        
    
]