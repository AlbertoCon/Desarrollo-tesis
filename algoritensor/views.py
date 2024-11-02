import os
from django.conf import settings
from myapp.models import iaimagen, ImagenHumana  # Importar los modelos de myapp
from .tensorflow_utils import cargar_datos, crear_modelo
from django.shortcuts import render
from django.http import JsonResponse
from tensorflow.keras.utils import load_img, img_to_array # type: ignore
from tensorflow.keras.models import load_model # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import numpy as np

# Create your views here.

def exportar_imagenes():
    # Directorios de salida
    ia_dir = os.path.join(settings.MEDIA_ROOT, 'dataset', 'ia')
    human_dir = os.path.join(settings.MEDIA_ROOT, 'dataset', 'human')

    # Crear directorios si no existen
    os.makedirs(ia_dir, exist_ok=True)
    os.makedirs(human_dir, exist_ok=True)

    # Exportar imágenes IA
    for imagen in iaimagen.objects.all():
        imagen_destino = os.path.join(ia_dir, os.path.basename(imagen.imagen.name))
        with open(imagen.imagen.path, 'rb') as f:
            with open(imagen_destino, 'wb') as dest:
                dest.write(f.read())

    # Exportar imágenes humanas
    for imagen in ImagenHumana.objects.all():
        imagen_destino = os.path.join(human_dir, os.path.basename(imagen.imagen.name))
        with open(imagen.imagen.path, 'rb') as f:
            with open(imagen_destino, 'wb') as dest:
                dest.write(f.read())

    print("Exportación completa.")


def entrenar_modelo(request):
    dataset = cargar_datos()
    model = crear_modelo()

    history = model.fit(dataset, epochs=10, validation_data=dataset)

    # Guardar el modelo entrenado
    model.save('media/modelo_ia_vs_humano.h5')

    return JsonResponse({'message': 'Modelo entrenado y guardado con éxito.'})


def predecir_imagen(request, img_path):
    model = load_model('media/modelo_ia_vs_humano.h5')

    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediccion = model.predict(img_array)
    resultado = "IA" if prediccion[0][0] >= 0.5 else "Humano"

    return JsonResponse({'resultado': resultado})