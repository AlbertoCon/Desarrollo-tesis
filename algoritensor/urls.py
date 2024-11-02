from django.urls import path
from .views import exportar_imagenes, entrenar_modelo, predecir_imagen

urlpatterns = [
    path('exportar/', exportar_imagenes, name='exportar_imagenes'),
    path('entrenar/', entrenar_modelo, name='entrenar_modelo'),
    path('predecir/<str:img_path>/', predecir_imagen, name='predecir_imagen'),
]
