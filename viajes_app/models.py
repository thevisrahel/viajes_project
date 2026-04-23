from django.db import models
from django.contrib.auth.models import User

class Viaje(models.Model):
    propietario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='viajes',
        null=True
    )

    region = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    sitio_turistico = models.CharField(max_length=150, blank=True, null=True)

    descripcion = models.TextField()
    fecha = models.DateField()
    imagen = models.ImageField(upload_to='viajes/', null=True, blank=True)

    def titulo_mostrar(self):
        return self.sitio_turistico if self.sitio_turistico else self.region


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'viaje')

    def __str__(self):
        return f'{self.user} ❤️ {self.viaje}'