from .models import SolicitudSeguimiento

def solicitudes_pendientes(request):
    if request.user.is_authenticated:
        count = SolicitudSeguimiento.objects.filter(
            destinatario=request.user,
            estado='pendiente'
        ).count()
        return {'solicitudes_pendientes_count': count}
    return {'solicitudes_pendientes_count': 0}