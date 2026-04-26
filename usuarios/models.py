from django.db import models                                               # Módulo base para definir modelos de BD
from django.contrib.auth.models import User                                # Modelo de usuario integrado de Django
from django.db.models.signals import post_save                             # Señal que se dispara después de guardar un modelo
from django.dispatch import receiver                                        # Decorador para conectar funciones a señales


class InfoExtra(models.Model):                                             # Modelo para almacenar información adicional del usuario
    user = models.OneToOneField(                                           # Relación uno a uno con el usuario
        User,                                                              # Modelo al que se vincula
        on_delete=models.CASCADE,                                          # Si se borra el usuario, se borra su InfoExtra también
        related_name="info"                                                # Permite acceder con request.user.info
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)             # Fecha de nacimiento opcional
    avatar = models.ImageField(                                            # Imagen de perfil del usuario
        upload_to="avatars/",                                              # Carpeta donde se guardan los avatars
        null=True,                                                         # Permite valor nulo en la BD
        blank=True,                                                        # Permite campo vacío en formularios
        default=None                                     
    )
    es_privado = models.BooleanField(default=False)                        # Si True, el perfil es privado

    def __str__(self):                                                     # Representación legible del objeto
        return self.user.username                                          # Muestra el nombre de usuario en el admin/shell


@receiver(post_save, sender=User)                                          # Se ejecuta automáticamente al guardar un User
def crear_info_extra(sender, instance, created, **kwargs):                 # Función que crea el InfoExtra asociado
    if created:                                                            # Solo si el usuario es nuevo (no en actualizaciones)
        InfoExtra.objects.create(user=instance)                            # Crea automáticamente el InfoExtra vinculado al usuario