from django.db import models                              # Importa el módulo de modelos de Django
from viajes_app.models import Viaje                       # Importa el modelo Viaje (relación)
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os


class Foto(models.Model):                                 # Modelo que representa una foto

    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)   # Relación muchos-a-uno con Viaje (si se borra el viaje, se borran sus fotos)

    imagen = models.ImageField(upload_to='fotos/')        # Campo para guardar la imagen (se almacena en /media/fotos/)

    def __str__(self):
        return f"Foto {self.id}"                          # Representación en texto del objeto (útil en admin y debugging)
    
@receiver(post_delete, sender=Foto)
def borrar_foto(sender, instance, **kwargs):
    if instance.imagen:
        if os.path.isfile(instance.imagen.path):
            os.remove(instance.imagen.path)