from django import forms                                                                          # Importa el módulo de formularios de Django
from django.contrib.auth.forms import (                                                           # Importa los formularios base de Django para autenticación
    UserCreationForm,                                                                             # Formulario base para crear usuarios
    PasswordChangeForm,                                                                           # Formulario base para cambiar contraseña
    AuthenticationForm,                                                                           # Formulario base para login
    SetPasswordForm,                                                                              # Formulario base para resetear contraseña desde link
    PasswordResetForm,                                                                            # Formulario base para solicitar reset por email
)
from django.contrib.auth.models import User                                                       # Importa el modelo User de Django
from .models import InfoExtra                                                                     # Importa el modelo InfoExtra para acceder a los datos extra del perfil


class LoginForm(AuthenticationForm):                                                              # Extiende el formulario de login de Django para personalizarlo
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                                                         # Llama al constructor original de Django

        self.fields["username"].label = "Usuario"                                                 # Cambia las etiquetas al español
        self.fields["password"].label = "Contraseña"

        self.fields["username"].help_text = ""                                                    # Elimina los textos de ayuda que Django agrega por defecto
        self.fields["password"].help_text = ""

        self.fields["username"].widget.attrs.update({                                             # Agrega clase Bootstrap y placeholder al campo usuario
            "class": "form-control",
            "placeholder": "Introduce tu usuario"
        })
        self.fields["password"].widget.attrs.update({                                             # Agrega clase Bootstrap y placeholder al campo contraseña
            "class": "form-control",
            "placeholder": "Introduce tu contraseña"
        })


class CreacionUsuario(UserCreationForm):                                                          # Extiende el formulario de creación de usuarios de Django
    class Meta:
        model = User                                                                              # Indica que el formulario está basado en el modelo User
        fields = [                                                                                # Campos que aparecerán en el formulario
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        ]
        widgets = {                                                                               # Widgets = personalización visual de los campos (HTML)
            "username":   forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
            "password1":  forms.PasswordInput(attrs={"class": "form-control"}),
            "password2":  forms.PasswordInput(attrs={"class": "form-control"}),
        }
        labels = {                                                                                # Etiquetas en español para cada campo
            "username":   "Nombre de usuario",
            "first_name": "Nombre",
            "last_name":  "Apellido",
            "email":      "Email",
            "password1":  "Contraseña",
            "password2":  "Repetir contraseña",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                                                         # Llama al constructor original de Django
        for field in self.fields.values():                                                        # Elimina los textos de ayuda que Django agrega por defecto
            field.help_text = ""


class ActualizarUsuario(forms.ModelForm):                                                         # Formulario para actualizar datos del usuario y su InfoExtra

    fecha_nacimiento = forms.DateField(                                                           # Campo extra que no está en User, pertenece a InfoExtra
        required=False,
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={
            "type": "date",                                                                       # Input tipo calendario en el navegador
            "class": "form-control"
        })
    )
    avatar = forms.ImageField(                                                                    # Campo extra para subir o cambiar la foto de perfil
        required=False,
        label="Avatar",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})                          # ClearableFileInput permite eliminar el avatar actual
    )

    class Meta:
        model = User                                                                              # El formulario base es el modelo User
        fields = ["first_name", "last_name", "email"]                                             # Solo estos campos del User son editables
        widgets = {                                                                               # Widgets = personalización visual de los campos (HTML)
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
        }
        labels = {                                                                                # Etiquetas en español para cada campo
            "first_name": "Nombre",
            "last_name":  "Apellido",
            "email":      "Email",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.get("instance")                                                             # Obtiene el usuario actual para cargar sus datos
        super().__init__(*args, **kwargs)                                                         # Llama al constructor original de Django

        for field in self.fields.values():                                                        # Elimina los textos de ayuda que Django agrega por defecto
            field.help_text = ""

        if user:
            info = InfoExtra.objects.get(user=user)                                               # Obtiene el InfoExtra del usuario (siempre existe gracias a la señal crear_info_extra)
            self.fields["fecha_nacimiento"].initial = info.fecha_nacimiento                       # Pre-rellena la fecha de nacimiento con el valor guardado
            self.fields["avatar"].initial = info.avatar                                           # Pre-rellena el avatar con el valor guardado

    def save(self, commit=True):
        user = super().save(commit=False)                                                         # Guarda el User sin hacer commit todavía para poder modificarlo

        fecha = self.cleaned_data.get("fecha_nacimiento")                                         # Obtiene la fecha limpia y validada del formulario
        avatar = self.cleaned_data.get("avatar")                                                  # Obtiene el avatar limpio y validado del formulario

        if commit:
            user.save()                                                                           # Guarda el User en la base de datos

        info = InfoExtra.objects.get(user=user)                                                   # Obtiene el InfoExtra (siempre existe gracias a la señal crear_info_extra)

        if fecha is not None:                                                                     # Solo actualiza la fecha si el usuario ingresó una
            info.fecha_nacimiento = fecha

        if avatar:                                                                                # Solo actualiza el avatar si el usuario subió uno nuevo
            info.avatar = avatar

        if commit:
            info.save()                                                                           # Guarda el InfoExtra en la base de datos

        return user                                                                               # Retorna el usuario actualizado


class CambiarPassword(PasswordChangeForm):                                                        # Extiende el formulario de cambio de contraseña de Django
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                                                         # Llama al constructor original de Django

        for field in self.fields.values():                                                        # Elimina los textos de ayuda que Django agrega por defecto
            field.help_text = ""

        labels = {                                                                                # Etiquetas en español para cada campo
            "old_password":  "Contraseña actual",
            "new_password1": "Nueva contraseña",
            "new_password2": "Confirmar nueva contraseña",
        }
        widgets = {                                                                               # Agrega clase Bootstrap a cada campo
            "old_password":  forms.PasswordInput(attrs={"class": "form-control"}),
            "new_password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "new_password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

        for field, label in labels.items():                                                       # Aplica etiquetas y widgets a cada campo
            self.fields[field].label = label
            self.fields[field].widget = widgets[field]


class ResetPasswordForm(SetPasswordForm):                                                         # Formulario para resetear contraseña desde el link del correo
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                                                         # Llama al constructor original de Django

        for field in self.fields.values():                                                        # Elimina los textos de ayuda que Django agrega por defecto
            field.help_text = ""

        labels = {                                                                                # Etiquetas en español para cada campo
            "new_password1": "Nueva contraseña",
            "new_password2": "Confirmar contraseña",
        }
        widgets = {                                                                               # Agrega clase Bootstrap a cada campo
            "new_password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "new_password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

        for field, label in labels.items():                                                       # Aplica etiquetas y widgets a cada campo
            self.fields[field].label = label
            self.fields[field].widget = widgets[field]


class PasswordResetEmailForm(PasswordResetForm):                                                  # Formulario para solicitar reset de contraseña con estilos Bootstrap
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)                                                         # Llama al constructor original de Django

        self.fields['email'].widget = forms.EmailInput(attrs={                                    # Aplica clase Bootstrap al campo email
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico'
        })
        self.fields['email'].label = 'Correo electrónico'                                        # Etiqueta en español
        self.fields['email'].help_text = ''                                                       # Elimina el texto de ayuda por defecto