from django.shortcuts import render, redirect                              # Funciones para renderizar templates y redirigir
from django.contrib.auth import login                                      # Función para iniciar sesión de un usuario
from usuarios.forms import CreacionUsuario, ActualizarUsuario              # Formularios personalizados de usuario
from django.contrib.auth.decorators import login_required                  # Decorador que exige autenticación
from django.contrib.auth.views import PasswordChangeView                   # Vista base para cambio de contraseña
from .forms import CambiarPassword, LoginForm                              # Formularios locales de login y cambio de pass
from django.urls import reverse_lazy                                       # URL diferida para usar en clases


def iniciar_sesion(request):                                               # Vista para iniciar sesión
    if request.method == "POST":                                           # Si el formulario fue enviado
        formulario = LoginForm(request, data=request.POST)                 # Instancia el formulario con los datos POST
        if formulario.is_valid():                                          # Valida credenciales
            user = formulario.get_user()                                   # Obtiene el usuario autenticado
            login(request, user)                                           # Inicia la sesión en Django
            return redirect("viajes_app:inicio")                           # Redirige al inicio
    else:                                                                  # Si es GET
        formulario = LoginForm()                                           # Formulario vacío
    return render(request, 'usuarios/iniciar_sesion.html', {               # Renderiza el template
        'formulario_iniciar_sesion': formulario                            # Pasa el formulario al contexto
    })

def registrarse(request):                                                  # Vista para registrar un nuevo usuario
    if request.method == "POST":                                           # Si el formulario fue enviado
        formulario = CreacionUsuario(request.POST)                         # Instancia con datos del POST
        if formulario.is_valid():                                          # Si los datos son válidos
            formulario.save()                                              # Guarda el nuevo usuario en la BD
            return redirect("usuarios:iniciar_sesion")                     # Redirige al login
    else:                                                                  # Si es GET
        formulario = CreacionUsuario()                                     # Formulario vacío
    return render(request, 'usuarios/registro.html', {                     # Renderiza el template de registro
        'formulario_registro': formulario                                  # Pasa el formulario al contexto
    })

@login_required                                                            # Solo usuarios autenticados pueden acceder
def perfil(request):                                                       # Vista del perfil del usuario actual
    seguidores = request.user.seguidores.count()                           # Cuenta los seguidores del usuario
    siguiendo = request.user.siguiendo.count()                             # Cuenta a quiénes sigue el usuario
    return render(request, 'usuarios/perfil.html', {                       # Renderiza el template del perfil
        'seguidores': seguidores,                                          # Envía el conteo de seguidores
        'siguiendo': siguiendo,                                            # Envía el conteo de siguiendo
    })

@login_required                                                            # Requiere autenticación
def actualizar_perfil(request):                                            # Vista para editar datos del perfil
    if request.method == "POST":                                           # Si se envió el formulario
        formulario = ActualizarUsuario(                                    # Instancia el formulario con:
            request.POST,                                                  # Datos del formulario
            request.FILES,                                                 # Archivos subidos (ej. avatar)
            instance=request.user                                          # Usuario actual a modificar
        )
        if formulario.is_valid():                                          # Si los datos son válidos
            formulario.save()                                              # Guarda los cambios en la BD
            return redirect('usuarios:perfil')                             # Redirige al perfil
    else:                                                                  # Si es GET
        formulario = ActualizarUsuario(instance=request.user)              # Formulario pre-cargado con datos actuales
    return render(request, 'usuarios/actualizar_perfil.html', {            # Renderiza el template
        'formulario': formulario                                           # Pasa el formulario al contexto
    })

@login_required
def eliminar_avatar(request):
    if request.method == "POST":
        info = request.user.info
        if info.avatar:
            info.avatar.delete(save=False)  # borra el archivo del disco
            info.avatar = None              # limpia el campo en la BD
            info.save()
    return redirect('usuarios:perfil')

class CambioDePass(PasswordChangeView):                                    # Vista basada en clase para cambiar contraseña
    template_name = 'usuarios/cambio_pass.html'                           # Template a usar
    form_class = CambiarPassword                                           # Formulario personalizado
    success_url = reverse_lazy('usuarios:perfil')                         # URL a la que redirige al tener éxito

@login_required                                                            # Requiere autenticación
def toggle_privacidad(request):                                            # Vista para alternar perfil público/privado
    if request.method == 'POST':                                           # Solo acepta POST
        info = request.user.info                                           # Obtiene el perfil extendido
        info.es_privado = not info.es_privado                             # Invierte el estado de privacidad
        info.save()                                                        # Guarda el cambio en la BD
    return redirect('usuarios:perfil')                                     # Redirige al perfil

@login_required                                                            # Requiere autenticación
def eliminar_perfil(request):                                              # Vista para eliminar la cuenta del usuario
    if request.method == 'POST':                                           # Si confirma la eliminación
        request.user.delete()                                              # Borra el usuario de la BD
        return redirect('usuarios:iniciar_sesion')                         # Redirige al login
    return render(request, 'usuarios/eliminar_perfil.html')                # Si es GET, muestra pantalla de confirmación

def about_me(request):                                                     # Vista pública de información del sitio
    return render(request, 'usuarios/about_me.html')                       # Renderiza el template about me