# myapp/forms.py
from django import forms
from .models import Imagen

class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['nombre', 'imagen']
