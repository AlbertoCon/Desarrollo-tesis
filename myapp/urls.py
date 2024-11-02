# myapp/urls.py
from django.urls import path
from .views import cargar_imagen, historial, configuracion,bdia, descargar_imagenes_zip, descargar_imagenes_clasificadas_zip


urlpatterns = [
    path('', cargar_imagen, name='cargar_imagen'),
    path('historial/', historial, name='historial'),
    path('configuracion/', configuracion, name='configuracion'),
    path('bdia/', bdia, name='bdia'),
    path('descargar_imagenes_zip/', descargar_imagenes_zip, name='descargar_imagenes_zip'),
    path('descargar_imagenes_clasificadas_zip/', descargar_imagenes_clasificadas_zip, name='descargar_imagenes_clasificadas_zip'),

]
