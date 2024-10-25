import http.client
import json
import mimetypes
from codecs import encode
from django.http import JsonResponse
from django.shortcuts import render
from .models import generalImagen

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

        return JsonResponse({
            'message': 'Imagen subida con éxito',
            'id': imagen_guardada.id,
            'resultado': resultado_json
        })

    return render(request, 'cargar_imagen.html')

def verificar_si_es_ia(imagen):
    """Función que se conecta con la API IA or NOT."""
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
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjRhZjhiZTYyLWIzMjAtNDE1YS05NzcyLTg0YzBlYWRlMzE5ZSIsInVzZXJfaWQiOiI0YWY4YmU2Mi1iMzIwLTQxNWEtOTc3Mi04NGMwZWFkZTMxOWUiLCJhdWQiOiJhY2Nlc3MiLCJleHAiOjAuMH0.-vlq_PuS0lcJ9vMw1sCu1IV5lgBf9sOYgB3EGJdAXjI',
        'Accept': 'application/json',
        'Content-type': f'multipart/form-data; boundary={boundary}'
    }

    conn.request("POST", "/v1/reports/image", body, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    return data.decode("utf-8")

def historial(request):
    imagenes = generalImagen.objects.all()
    return render(request, 'historial.html', {'imagenes': imagenes})

def configuracion(request):
    return render(request, 'configuracion.html')
