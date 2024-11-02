import os
import http.client
import json
import mimetypes
from codecs import encode
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import generalImagen, iaimagen, ImagenHumana, iaimagenverdos
import zipfile
from django.conf import settings


def cargar_imagen(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No se subió ningún archivo'}, status=400)

        nombre = request.FILES['file'].name
        imagen = request.FILES['file']

        # Verificar con la API si es IA o Humano
        resultado_api = verificar_si_es_ia(imagen)
        try:
            resultado_json = json.loads(resultado_api)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Respuesta inválida de la API', 'detalle': str(e)}, status=500)

        # Determinar el tipo (IA o Humano)
        tipo = 'ai' if resultado_json['report']['verdict'] == 'ai' else 'human'

        # Guardar en el modelo generalImagen
        imagen_guardada = generalImagen.objects.create(nombre=nombre, imagen=imagen, tipo=tipo)

        if tipo == 'ai':
            # Guardar en el modelo ImagenIA y marcar la imagen
            imagen_guardada = iaimagenverdos.objects.create(nombre=nombre, imagen=imagen)
            imagen_guardada.marcar_imagen()  # Agregar el sello a la imagen
        else:
            # Guardar en el modelo ImagenHumana
            imagen_guardada = ImagenHumana.objects.create(nombre=nombre, imagen=imagen)

        return JsonResponse({
            'message': 'Imagen subida con éxito',
            'id': imagen_guardada.id,
            'resultado': resultado_json,
        })

    return render(request, 'cargar_imagen.html')

def verificar_si_es_ia(imagen):
    conn = http.client.HTTPSConnection("api.aiornot.com")
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList = []

    dataList.append(encode('--' + boundary))
    dataList.append(encode(f'Content-Disposition: form-data; name=object; filename={imagen.name}'))

    fileType = mimetypes.guess_type(imagen.name)[0] or 'application/octet-stream'
    dataList.append(encode(f'Content-Type: {fileType}'))
    dataList.append(encode(''))

    dataList.append(imagen.read())
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))

    body = b'\r\n'.join(dataList)

    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQwY2JmNDA1LTBhZWUtNDQ2Yi1hZWZjLTc2NWIzNDBkNDZlNyIsInVzZXJfaWQiOiJkMGNiZjQwNS0wYWVlLTQ0NmItYWVmYy03NjViMzQwZDQ2ZTciLCJhdWQiOiJhY2Nlc3MiLCJleHAiOjAuMH0.oqJr5VSgaUVGE6EMCjD1CnQFQ40moxCFt4twkd0TQYQ',
        'Accept': 'application/json',
        'Content-type': f'multipart/form-data; boundary={boundary}'
    }

    conn.request("POST", "/v1/reports/image", body, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    return data.decode("utf-8")



def descargar_imagenes_zip(request):
    # Crear un archivo ZIP temporal
    zip_path = os.path.join(settings.BASE_DIR, 'imagenes.zip')
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        # Agregar cada imagen al archivo ZIP
        for imagen in iaimagenverdos.objects.all():  # Cambia el modelo si es necesario
            imagen_path = os.path.join(settings.MEDIA_ROOT, imagen.imagen.name)
            zip_file.write(imagen_path, os.path.basename(imagen_path))

    # Leer el archivo ZIP y enviarlo en la respuesta
    with open(zip_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="imagenes.zip"'
        return response




def descargar_imagenes_clasificadas_zip(request):
    # Crear un archivo ZIP temporal
    zip_path = os.path.join(settings.BASE_DIR, 'imagenes_clasificadas.zip')
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        # Filtrar y agregar imágenes de tipo "humano" a la carpeta "humanas" dentro del ZIP
        for imagen in generalImagen.objects.filter(tipo="human"):
            imagen_path = os.path.join(settings.MEDIA_ROOT, imagen.imagen.name)
            zip_file.write(imagen_path, f"humanas/{os.path.basename(imagen_path)}")

        # Filtrar y agregar imágenes de tipo "IA" a la carpeta "IA" dentro del ZIP
        for imagen in generalImagen.objects.filter(tipo="ai"):
            imagen_path = os.path.join(settings.MEDIA_ROOT, imagen.imagen.name)
            zip_file.write(imagen_path, f"IA/{os.path.basename(imagen_path)}")

    # Leer el archivo ZIP y enviarlo en la respuesta
    with open(zip_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename="imagenes_clasificadas.zip"'
        return response


def historial(request):
    imagenes = generalImagen.objects.all()
    return render(request, 'historial.html', {'imagenes': imagenes})


def bdia(request):
    imagenes = iaimagenverdos.objects.all()
    return render(request, 'bdia.html', {'imagenes': imagenes})


def configuracion(request):
    return render(request, 'configuracion.html')
