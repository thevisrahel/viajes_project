from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from usuarios.forms import CreacionUsuario, ActualizarUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from .forms import CambiarPassword, LoginForm
from django.contrib.auth.models import User
from .models import InfoExtra, Seguimiento, SolicitudSeguimiento
from viajes_app.models import Viaje, Like

def iniciar_sesion(request):

    if request.method == "POST":
        formulario = LoginForm(request, data=request.POST)

        if formulario.is_valid():
            user = formulario.get_user()
            login(request, user)
            return redirect("viajes_app:inicio")

    else:
        formulario = LoginForm()

    return render(request, 'usuarios/iniciar_sesion.html', {
        'formulario_iniciar_sesion': formulario
    })
    
def registrarse(request):
    
    if request.method == "POST":
        formulario = CreacionUsuario(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect("usuarios:iniciar_sesion")
    else:
        formulario = CreacionUsuario()
        
    return render(request, 'usuarios/registro.html', {'formulario_registro': formulario})

@login_required
def perfil(request):
    seguidores = request.user.seguidores.count()
    siguiendo = request.user.siguiendo.count()
    return render(request, 'usuarios/perfil.html', {
        'seguidores': seguidores,
        'siguiendo': siguiendo,
    })

@login_required
def actualizar_perfil(request):
    if request.method == "POST":
        print("=== DEBUG ===")
        print("FILES:", request.FILES)
        print("POST:", request.POST)
        
        formulario = ActualizarUsuario(
            request.POST,
            request.FILES, 
            instance=request.user
        )
        
        print("Form valid:", formulario.is_valid())
        print("Form errors:", formulario.errors)
        
        if formulario.is_valid():
            print("cleaned avatar:", formulario.cleaned_data.get("avatar"))
            formulario.save()
            return redirect('usuarios:perfil')
    else:
        formulario = ActualizarUsuario(instance=request.user)

    return render(request, 'usuarios/actualizar_perfil.html', {
        'formulario': formulario
    })
    
@login_required
def eliminar_avatar(request):
    if request.method == "POST":
        info = request.user.info
        if info.avatar:
            info.avatar.delete()
            info.save()
    return redirect('usuarios:perfil')

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView


class CambioDePass(PasswordChangeView):
    template_name = 'usuarios/cambio_pass.html'
    form_class = CambiarPassword
    success_url = reverse_lazy('usuarios:perfil')
    
    

def buscar_usuarios(request):
    query = request.GET.get('q')
    resultados = []

    if query:
        resultados = User.objects.filter(username__icontains=query)

        # opcional: excluirte a ti mismo
        if request.user.is_authenticated:
            resultados = resultados.exclude(id=request.user.id)

    return render(request, 'usuarios/buscar_usuarios.html', {
        'resultados': resultados,
        'query': query
    })
    

def ver_perfil(request, username):
    usuario = get_object_or_404(User, username=username)
    InfoExtra.objects.get_or_create(user=usuario) 
    viajes = []
    es_seguidor = False
    es_privado = usuario.info.es_privado

    if request.user.is_authenticated:
        es_seguidor = Seguimiento.objects.filter(
            seguidor=request.user, seguido=usuario
        ).exists()

    if not es_privado or es_seguidor or request.user == usuario:
        viajes = usuario.viajes.order_by('-fecha')


    seguidores = usuario.seguidores.count()
    siguiendo = usuario.siguiendo.count()

    solicitud_pendiente = SolicitudSeguimiento.objects.filter(
        solicitante=request.user,
        destinatario=usuario,
        estado='pendiente'
        
    ).exists() if request.user.is_authenticated else False

    return render(request, 'usuarios/ver_perfil.html', {
        'usuario': usuario,
        'viajes': viajes,
        'es_seguidor': es_seguidor,
        'es_privado': es_privado,
        'seguidores': seguidores,
        'siguiendo': siguiendo,
        'solicitud_pendiente': solicitud_pendiente,
    })
    
@login_required
def seguir(request, username):
    usuario_a_seguir = get_object_or_404(User, username=username)
    if request.user == usuario_a_seguir:
        return redirect('usuarios:ver_perfil', username=username)

    SolicitudSeguimiento.objects.get_or_create(
        solicitante=request.user,
        destinatario=usuario_a_seguir
    )

    return redirect('usuarios:ver_perfil', username=username)

@login_required
def dejar_de_seguir(request, username):
    usuario_a_dejar = get_object_or_404(User, username=username)
    Seguimiento.objects.filter(seguidor=request.user, seguido=usuario_a_dejar).delete()
    # También cancelar solicitud pendiente si existiera
    SolicitudSeguimiento.objects.filter(solicitante=request.user, destinatario=usuario_a_dejar).delete()
    return redirect('usuarios:ver_perfil', username=username)

@login_required
def solicitudes(request):
    solicitudes_pendientes = request.user.solicitudes_recibidas.filter(estado='pendiente')
    return render(request, 'usuarios/solicitudes.html', {
        'solicitudes': solicitudes_pendientes
    })

@login_required
def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSeguimiento, id=solicitud_id, destinatario=request.user)
    solicitud.estado = 'aceptada'
    solicitud.save()
    Seguimiento.objects.get_or_create(seguidor=solicitud.solicitante, seguido=request.user)
    return redirect('usuarios:solicitudes')

@login_required
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSeguimiento, id=solicitud_id, destinatario=request.user)
    solicitud.delete()
    return redirect('usuarios:solicitudes')

@login_required
def toggle_privacidad(request):
    if request.method == 'POST':
        info = request.user.info
        info.es_privado = not info.es_privado
        info.save()
    return redirect('usuarios:perfil')


def detalle_viaje_publico(request, username, id_viaje):
    usuario = get_object_or_404(User, username=username)
    viaje = get_object_or_404(Viaje, id=id_viaje, propietario=usuario)

    es_privado = usuario.info.es_privado
    es_seguidor = Seguimiento.objects.filter(
        seguidor=request.user,
        seguido=usuario
    ).exists() if request.user.is_authenticated else False

    if es_privado and not es_seguidor and request.user != usuario:
        return redirect('usuarios:ver_perfil', username=username)

    # 🔥 AQUI ESTÁ LO QUE TE FALTABA
    usuario_dio_like = False
    if request.user.is_authenticated:
        usuario_dio_like = viaje.likes.filter(id=request.user.id).exists()

    return render(request, 'usuarios/detalle_viaje_publico.html', {
        'usuario': usuario,
        'viaje': viaje,
        'usuario_dio_like': usuario_dio_like,  # 👈 IMPORTANTE
    })
    
def lista_seguidores(request, username):
    usuario = get_object_or_404(User, username=username)
    
    es_privado = usuario.info.es_privado
    es_seguidor = Seguimiento.objects.filter(
        seguidor=request.user, seguido=usuario
    ).exists() if request.user.is_authenticated else False

    if es_privado and not es_seguidor and request.user != usuario:
        return redirect('usuarios:ver_perfil', username=username)

    seguidores = User.objects.filter(siguiendo__seguido=usuario)
    return render(request, 'usuarios/lista_seguidores.html', {
        'usuario': usuario,
        'usuarios': seguidores,
        'titulo': f'Seguidores de {usuario.username}'
    })


def lista_siguiendo(request, username):
    usuario = get_object_or_404(User, username=username)

    es_privado = usuario.info.es_privado
    es_seguidor = Seguimiento.objects.filter(
        seguidor=request.user, seguido=usuario
    ).exists() if request.user.is_authenticated else False

    if es_privado and not es_seguidor and request.user != usuario:
        return redirect('usuarios:ver_perfil', username=username)

    siguiendo = User.objects.filter(seguidores__seguidor=usuario)
    return render(request, 'usuarios/lista_seguidores.html', {
        'usuario': usuario,
        'usuarios': siguiendo,
        'titulo': f'{usuario.username} sigue a'
    })