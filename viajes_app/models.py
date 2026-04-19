from django.db import models

class Viaje(models.Model):
    destino = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    imagen = models.ImageField(upload_to='viajes/', null=True, blank=True)
    
    def __str__(self):
        return f'Viaje: {self.destino}'