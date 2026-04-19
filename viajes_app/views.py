from django.shortcuts import render, redirect, get_object_or_404
from .models import Viaje
from .forms import ViajeForm

def inicio(request):
    return render(request, 'viajes_app/inicio.html')


def crear_viaje(request):
    mensaje = ""

    if request.method == "POST":
        form = ViajeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            mensaje = "Viaje creado correctamente"
            form = ViajeForm()
    else:
        form = ViajeForm()

    return render(request, 'viajes_app/crear_viaje.html', {
        'form': form,
        'mensaje': mensaje
    })

def listar_viajes(request):
    query = request.GET.get('q')

    if query:
        viajes = Viaje.objects.filter(destino__icontains=query)
    else:
        viajes = Viaje.objects.all()

    return render(request, 'viajes_app/listar_viajes.html', {
        'viajes': viajes,
        'query': query
    })
    
def detalle_viajes(request, id_viaje):
    viaje = Viaje.objects.get(id=id_viaje)
    return render(request, 'viajes_app/detalle_viajes.html', {'viaje': viaje})



def actualizar_viajes(request, id_viaje):
    viaje = get_object_or_404(Viaje, id=id_viaje)

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

def eliminar_viajes(request, id_viaje):
    viaje = get_object_or_404(Viaje, id=id_viaje)
    viaje.delete()
    return redirect('viajes_app:listar_viajes')