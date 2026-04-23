from django.shortcuts import render, redirect, get_object_or_404
from .models import Viaje
from .forms import ViajeForm
from django.contrib.auth.decorators import login_required
from .models import Viaje, Like

def inicio(request):
    return render(request, 'viajes_app/inicio.html')


@login_required
def crear_viaje(request):
    mensaje = ""

    if request.method == "POST":
        form = ViajeForm(request.POST, request.FILES)

        if form.is_valid():
            viaje = form.save(commit=False)
            viaje.propietario = request.user  # asigna el usuario logueado
            viaje.save()

            mensaje = "Viaje creado correctamente"
            form = ViajeForm()  # limpia el formulario después de guardar

    else:
        form = ViajeForm()

    return render(request, 'viajes_app/crear_viaje.html', {
        'form': form,
        'mensaje': mensaje
    })
    
@login_required
def listar_viajes(request):
    query = request.GET.get('q')

    if query:
        viajes = Viaje.objects.filter(propietario=request.user, destino__icontains=query) 
    else:
        viajes = Viaje.objects.filter(propietario=request.user) 

    return render(request, 'viajes_app/listar_viajes.html', {
        'viajes': viajes,
        'query': query
    })
    
@login_required    
def detalle_viajes(request, id_viaje):
    viaje = get_object_or_404(Viaje, id=id_viaje, propietario=request.user)  
    return render(request, 'viajes_app/detalle_viajes.html', {'viaje': viaje})

@login_required
def actualizar_viajes(request, id_viaje):
    viaje = get_object_or_404(Viaje, id=id_viaje, propietario=request.user)

    if request.method == "POST":
        formulario = ViajeForm(request.POST, request.FILES, instance=viaje)
        if formulario.is_valid():
            formulario.save()
            return redirect('viajes_app:listar_viajes')
    else:
        formulario = ViajeForm(instance=viaje)

    return render(request, 'viajes_app/actualizar_viajes.html', {
        'formulario': formulario,
        'viaje': viaje
    })
    
@login_required
def eliminar_viajes(request, id_viaje):
    viaje = get_object_or_404(Viaje, id=id_viaje, propietario=request.user)  
    viaje.delete()
    return redirect('viajes_app:listar_viajes')

@login_required
def toggle_like(request, viaje_id):
    viaje = get_object_or_404(Viaje, id=viaje_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        viaje=viaje
    )

    if not created:
        like.delete()

    return redirect('usuarios:detalle_viaje_publico',
        username=viaje.propietario.username,
        id_viaje=viaje.id
)

