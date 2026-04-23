from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from usuarios.views import CambioDePass
from django.urls import reverse_lazy

app_name = 'usuarios'

urlpatterns = [
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar-sesion/', LogoutView.as_view(template_name='usuarios/cerrar_sesion.html'), name='cerrar_sesion'),  
    path('registro/', views.registrarse, name='registro'),    
    path('perfil/', views.perfil, name='perfil'), 
    path('perfil/actualizar', views.actualizar_perfil, name='actualizar_perfil'), 
    path('perfil/eliminar-avatar/', views.eliminar_avatar, name='eliminar_avatar'),
    path('perfil/actualizar/password/', CambioDePass.as_view(), name='actualizar_password'),
    path('buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    path('privacidad/', views.toggle_privacidad, name='toggle_privacidad'),  # 👈 antes de <str:username>

    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='usuarios/password_reset.html',
            email_template_name='usuarios/password_reset_email.html',
            success_url=reverse_lazy('usuarios:password_reset_done')
        ),
        name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'),
         name='password_reset_complete'),


    path('solicitudes/', views.solicitudes, name='solicitudes'),
    path('solicitudes/<int:solicitud_id>/aceptar/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('solicitudes/<int:solicitud_id>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('<str:username>/', views.ver_perfil, name='ver_perfil'),
    path('<str:username>/viaje/<int:id_viaje>/', views.detalle_viaje_publico, name='detalle_viaje_publico'),
    path('<str:username>/seguir/', views.seguir, name='seguir'),
    path('<str:username>/dejar-de-seguir/', views.dejar_de_seguir, name='dejar_de_seguir'),
    path('<str:username>/seguidores/', views.lista_seguidores, name='lista_seguidores'),
    path('<str:username>/siguiendo/', views.lista_siguiendo, name='lista_siguiendo'),
]