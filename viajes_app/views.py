from django.shortcuts import render, redirect, get_object_or_404                                                        # Funciones útiles para renderizar templates y manejar redirecciones
from .models import Viaje, Like                                                                                         # Importamos los modelos
from .forms import ViajeForm                                                                                            # Importamos el formulario
from django.contrib.auth.decorators import login_required                                                               # Para proteger vistas (solo usuarios logueados)
from django.db.models import Q


def inicio(request):                                                                                                    # Renderiza la página principal
    return render(request, 'viajes_app/inicio.html')

@login_required                                                                                                         # Solo usuarios autenticados pueden acceder
def crear_viaje(request):
                                                                                     

    if request.method == "POST":                                                                                        
        form = ViajeForm(request.POST, request.FILES)                                                                   # Se envía el formulario con datos + archivos (imagen)

        if form.is_valid():                     
            viaje = form.save(commit=False)                                                                             # commit=False → permite modificar el objeto antes de guardarlo
            viaje.propietario = request.user                                                                            # Se asigna el usuario actual como propietario
            viaje.save()                                                                                                # Guardado final en base de datos
                                                      
            form = ViajeForm()                                                                                          # Se reinicia el formulario para permitir crear otro viaje

    else:                                                                                                               # Petición GET → formulario vacío
        form = ViajeForm()

    return render(request, 'viajes_app/crear_viaje.html', {                                                             # DEVUELVO LA PÁGINA
        'form': form,                                                                                                   # Le envío al HTML: el formulario
    })
    
@login_required
def listar_viajes(request):
    query = request.GET.get('q')

    if query:
        viajes = Viaje.objects.filter(
            propietario=request.user
        ).filter(
            Q(sitio_turistico__icontains=query) |
            Q(region__icontains=query) |
            Q(pais__icontains=query)
        )
    else:
        viajes = Viaje.objects.filter(propietario=request.user)

    return render(request, 'viajes_app/listar_viajes.html', {
        'viajes': viajes,
        'query': query
    })
    
@login_required                                                                                                         # Solo usuarios autenticados pueden acceder
def detalle_viajes(request, id_viaje):                                                                                  # id_viaje viene de la URL, ej: /viajes/5/
    viaje = get_object_or_404(Viaje, id=id_viaje, propietario=request.user)                                             # Busca el viaje por id Y que sea del usuario, si no existe retorna 404
    return render(request, 'viajes_app/detalle_viajes.html', {                                                          # Renderiza el template con el viaje encontrado
        'viaje': viaje,                                                                                                 # El viaje a mostrar
    })
    
@login_required                                                                                                         # Solo usuarios autenticados pueden acceder
def actualizar_viajes(request, id_viaje):                                                                               # id_viaje viene de la URL
    viaje = get_object_or_404(Viaje, id=id_viaje, propietario=request.user)                                             # Busca el viaje, si no existe o no es del usuario retorna 404

    if request.method == "POST":                                                                                        # Si el usuario envió el formulario
        form = ViajeForm(request.POST, request.FILES, instance=viaje)                                                   # Crea el formulario con los datos enviados y el viaje existente
        if form.is_valid():                                                                                             # Si todos los campos son válidos
            form.save()                                                                                                 # Guarda los cambios en la base de datos
            return redirect('viajes_app:listar_viajes')                                                                 # Redirige al listado de viajes
                                                                                                                        # Si el formulario es inválido, cae aquí y el template mostrará los errores automáticamente
    else:                                                                                                               # Si el usuario solo está visitando la página (GET)
        form = ViajeForm(instance=viaje)                                                                                # Muestra el formulario con los datos actuales del viaje

    return render(request, 'viajes_app/actualizar_viajes.html', {
        'formulario': form,                                                                                             # El formulario para mostrar en el template (incluye errores si los hay)
        'viaje': viaje                                                                                                  # El viaje actual, útil para mostrar info extra en el template
    })                             

@login_required                                                                                                         # Solo usuarios autenticados pueden acceder
def eliminar_viajes(request, id_viaje):                                                                                 # id_viaje viene de la URL
    viaje = get_object_or_404(Viaje, id=id_viaje, propietario=request.user)                                             # Busca el viaje, si no existe o no es del usuario retorna 404
    if request.method == "POST":                                                                                        # Solo elimina si es una acción intencional (POST)
        viaje.delete()                                                                                                  # Elimina el viaje de la base de datos
        return redirect('viajes_app:listar_viajes')                                                                     # Redirige al listado de viajes
    return redirect('viajes_app:listar_viajes')                                                                         # Si alguien entra por GET, redirige sin romper nada

@login_required                                                                                                         # Solo usuarios autenticados pueden acceder
def toggle_like(request, viaje_id):                                                                                     # viaje_id viene de la URL
    if request.method == "POST":                                                                                        # Solo procesa el like si es una acción intencional (POST)
        viaje = get_object_or_404(Viaje, id=viaje_id)                                                                   # Busca el viaje, si no existe retorna 404 (cualquier usuario puede dar like)
        like, created = Like.objects.get_or_create(                                                                     # Intenta obtener el like, si no existe lo crea
            user=request.user,                                                                                          # Del usuario actual
            viaje=viaje                                                                                                 # Para este viaje
        )
        if not created:                                                                                                 # Si 'created' es False significa que el like ya existía
            like.delete()                                                                                               # Lo elimina (toggle: si existe lo quita, si no existe lo crea)

    return redirect('social:detalle_viaje_publico',                                                                   # Redirige al detalle público del viaje
        username=viaje.propietario.username,                                                                            # Pasando el username del propietario
        id_viaje=viaje.id                                                                                               # Y el id del viaje
    )