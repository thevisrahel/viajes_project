from django.urls import path                                               # Función para definir rutas URL
from . import views                                                        # Importa las vistas del módulo actual
from django.contrib.auth import views as auth_views                        # Vistas de autenticación integradas de Django
from .views import CambioDePass                                            # Vista de cambio de contraseña personalizada
from .forms import CambiarPassword, ResetPasswordForm, PasswordResetEmailForm  # Formularios personalizados con estilos Bootstrap

app_name = 'usuarios'                                                      # Namespace de la app para usar en reverse/redirect

urlpatterns = [

    # ---------------- AUTENTICACIÓN ----------------
    path('iniciar-sesion/',                                                # Login del usuario
         views.iniciar_sesion,
         name='iniciar_sesion'),

    path('cerrar-sesion/',                                                 # URL para cerrar sesión
         auth_views.LogoutView.as_view(template_name='usuarios/cerrar_sesion.html'),
         name='cerrar_sesion'),

    path('registro/',                                                      # Registro de nuevo usuario
         views.registrarse,
         name='registro'),


    # ---------------- RECUPERACIÓN DE CONTRASEÑA ----------------
    path('password-reset/',                                                # URL para solicitar reseteo de contraseña
         auth_views.PasswordResetView.as_view(
             template_name='usuarios/password_reset_form.html',           # Template del formulario de reset
             email_template_name='usuarios/password_reset_email.html',    # Template del email que se envía al usuario
             form_class=PasswordResetEmailForm,                           # Formulario con estilos Bootstrap
             extra_email_context={'domain': '127.0.0.1:8000', 'protocol': 'http'}, # Fuerza el dominio correcto
             success_url='/usuarios/password-reset/done/'                 # Redirige aquí tras enviar el email
         ),
         name='password_reset'),

    path('password-reset/done/',                                           # URL de confirmación de email enviado
         auth_views.PasswordResetDoneView.as_view(
             template_name='usuarios/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',                                        # URL con token único para confirmar el reset
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/password_reset_confirm.html',        # Template del formulario de nueva contraseña
             form_class=ResetPasswordForm,                                 # Formulario con estilos Bootstrap
             reset_url_token='set-password',                              # Token de sesión de Django 6
             success_url='/usuarios/reset/done/'                          # Redirige aquí tras cambiar la contraseña
         ),
         name='password_reset_confirm'),

    path('reset/done/',                                                    # URL final: reset completado con éxito
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usuarios/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    # ---------------- PERFIL ----------------
    path('perfil/',                                                        # Ver perfil propio
         views.perfil,
         name='perfil'),

    path('perfil/actualizar/',                                             # Editar datos del perfil
         views.actualizar_perfil,
         name='actualizar_perfil'),

    path('perfil/actualizar/password/',                                    # Cambiar contraseña estando logueado
         CambioDePass.as_view(),
         name='actualizar_password'),

    path('perfil/eliminar-avatar/',                                        # Eliminar avatar personalizado
         views.eliminar_avatar,
         name='eliminar_avatar'),

    path('privacidad/',                                                    # Alternar perfil público/privado
         views.toggle_privacidad,
         name='toggle_privacidad'),

    path('eliminar-perfil/',                                               # Eliminar cuenta del usuario
         views.eliminar_perfil,
         name='eliminar_perfil'),


    # ---------------- GENERAL ----------------
    path('about-me/',                                                      # Página informativa sobre el sitio
         views.about_me,
         name='about_me'),
]