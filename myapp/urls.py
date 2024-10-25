# myapp/urls.py
from django.urls import path
from .views import cargar_imagen, historial, configuracion

urlpatterns = [
    path('', cargar_imagen, name='cargar_imagen'),
    path('historial/', historial, name='historial'),
    path('configuracion/', configuracion, name='configuracion'),
]
