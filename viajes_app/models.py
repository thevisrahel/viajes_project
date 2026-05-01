from django.db import models
from django.contrib.auth.models import User                                                         # Modelo de usuario que trae Django por defecto
from django.utils import timezone
import os
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Viaje(models.Model):                                                                          # Representa un viaje publicado por un usuario
    propietario = models.ForeignKey(                                                                # ForeignKey = relación muchos a uno (un usuario puede tener muchos viajes)
        User,   
        on_delete=models.CASCADE,                                                                   # on_delete=CASCADE → si se elimina el usuario, se eliminan todos sus viajes
        related_name='viajes'                                                                       # related_name='viajes' → permite acceder a los viajes de un usuario con: usuario.viajes.all(                                                                           # un viaje puede existir sin propietario (huérfano)
    )

    region = models.CharField(max_length=100)                                                       # Campo de texto corto (máx 100 caracteres) para la región
    pais = models.CharField(max_length=100)                                                         # Campo de texto para el país
    sitio_turistico = models.CharField(max_length=150, blank=True, null=True)                       # Campo opcional (puede estar vacío)

    descripcion = models.TextField()                                                                # Texto largo, ideal para descripciones extensas
    fecha = models.DateField()                                                                      # Fecha del viaje (no de creación)
    imagen = models.ImageField(upload_to='viajes/', null=True, blank=True)                          # Campo para subir imágenes, es un campo opcional

    creado = models.DateTimeField(auto_now_add=True)                                                # Guarda automáticamente cuándo se creó el viaje
  
    actualizado = models.DateTimeField(auto_now=True)                                               # Se actualiza cada vez que se modifica

    total_likes = models.PositiveIntegerField(default=0)                                            # Contador de likes

    def titulo_mostrar(self):                                                                       # Método personalizado (no es un campo). Sirve para mostrar un título dinámico del viaje
        return self.sitio_turistico if self.sitio_turistico else self.region                        # Si existe sitio turístico → lo muestra, Si no → muestra la región
    
    def __str__(self):                                                                              # Mejor representación
            return f"{self.titulo_mostrar()} - {self.propietario.username}"
    class Meta:
        ordering = ['-fecha']                                                                       # Se ordena por fecha de viaje

class Like(models.Model):

    user = models.ForeignKey(                                                                       
        User,
        on_delete=models.CASCADE,                                                                   # Si se elimina el usuario → se eliminan sus likes automáticamente
        related_name='likes'                                                                        # Permite acceder desde el usuario: user.likes.all() → todos los likes que ha dado
    )

    viaje = models.ForeignKey(                                                                      
        Viaje,  
        on_delete=models.CASCADE,                                                                   # Si se elimina el viaje → se eliminan sus likes
        related_name='likes'                                                                        # Permite acceder desde el viaje:
    )

    creado = models.DateTimeField(default=timezone.now)                                               # Guarda automáticamente la fecha y hora cuando se crea el like
  
    class Meta:                                                                                     # Evita que un usuario dé like más de una vez al mismo viaje
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'viaje'],
                name='unique_like'
            )
        ]

    def __str__(self):                                                                              # Define cómo se muestra el objeto en: - Django admin - consola (print)
        return f'{self.user.username} ❤️ {self.viaje.titulo_mostrar()}'
    
    
    
    
@receiver(post_delete, sender=Viaje)
def borrar_imagen_viaje(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)