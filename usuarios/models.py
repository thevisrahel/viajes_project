from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class InfoExtra(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="info"
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    es_privado = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Seguimiento(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='siguiendo')
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidores')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seguidor', 'seguido')

    def __str__(self):
        return f'{self.seguidor} sigue a {self.seguido}'
    
class SolicitudSeguimiento(models.Model):
    DE_PENDIENTE = 'pendiente'
    DE_ACEPTADA = 'aceptada'
    DE_RECHAZADA = 'rechazada'

    ESTADOS = [
        (DE_PENDIENTE, 'Pendiente'),
        (DE_ACEPTADA, 'Aceptada'),
        (DE_RECHAZADA, 'Rechazada'),
    ]

    solicitante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes_recibidas')
    estado = models.CharField(max_length=10, choices=ESTADOS, default=DE_PENDIENTE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('solicitante', 'destinatario')

    def __str__(self):
        return f'{self.solicitante} → {self.destinatario} ({self.estado})'
    
@receiver(post_save, sender=User)
def crear_info_extra(sender, instance, created, **kwargs):
    if created:
        InfoExtra.objects.get_or_create(user=instance)
        
