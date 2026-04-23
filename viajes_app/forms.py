from django import forms
from .models import Viaje

class ViajeForm(forms.ModelForm):

    class Meta:
        model = Viaje
        fields = [
            'region',
            'pais',
            'sitio_turistico',
            'descripcion',
            'fecha',
            'imagen'
        ]

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }