# myapp/views.py
from django.http import JsonResponse
from django.shortcuts import render
from .models import Imagen

def cargar_imagen(request):
    if request.method == 'POST':
        # Validar si se subió un archivo
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No se subió ningún archivo'}, status=400)

        # Crear una instancia del modelo y guardar la imagen
        imagen = Imagen.objects.create(
            nombre=request.FILES['file'].name,  # Usa el nombre del archivo como 'nombre'
            imagen=request.FILES['file']
        )

        return JsonResponse({'message': 'Imagen subida con éxito', 'id': imagen.id})

    return render(request, 'cargar_imagen.html')
