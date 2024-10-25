# myapp/urls.py
from django.urls import path
from .views import cargar_imagen

urlpatterns = [
    path('', cargar_imagen, name='cargar_imagen'),
]
