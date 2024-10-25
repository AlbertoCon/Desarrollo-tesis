# myapp/views.py
import http.client
import json
import mimetypes
from codecs import encode
from django.http import JsonResponse
from django.shortcuts import render
from .models import Imagen

def cargar_imagen(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No se subió ningún archivo'}, status=400)

        imagen = Imagen.objects.create(
            nombre=request.FILES['file'].name,
            imagen=request.FILES['file']
        )

        resultado_api = verificar_si_es_ia(imagen.imagen.path)

        try:
            resultado_json = json.loads(resultado_api)  # Asegúrate que es un JSON válido
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Respuesta inválida de la API', 'detalle': str(e)}, status=500)

        return JsonResponse({
            'message': 'Imagen subida con éxito',
            'id': imagen.id,
            'resultado': resultado_json
        })

    return render(request, 'cargar_imagen.html')

def verificar_si_es_ia(ruta_imagen):
    """Función que se conecta con la API IA or NOT para verificar si la imagen es generada por IA."""
    conn = http.client.HTTPSConnection("api.aiornot.com")
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList = []

    dataList.append(encode('--' + boundary))
    dataList.append(encode(f'Content-Disposition: form-data; name=object; filename={ruta_imagen}'))

    fileType = mimetypes.guess_type(ruta_imagen)[0] or 'application/octet-stream'
    dataList.append(encode(f'Content-Type: {fileType}'))
    dataList.append(encode(''))

    with open(ruta_imagen, 'rb') as f:
        dataList.append(f.read())

    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))

    body = b'\r\n'.join(dataList)

    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjMyYjJkMTRlLTA3ZmEtNDY4Yy05YTc1LTBjYjI5MzdhNzNjMSIsInVzZXJfaWQiOiIzMmIyZDE0ZS0wN2ZhLTQ2OGMtOWE3NS0wY2IyOTM3YTczYzEiLCJhdWQiOiJhY2Nlc3MiLCJleHAiOjAuMH0.bg6LTEl5XkdvfMssfcyK087UZQtUX77MS3kMnfK4vRc',
        'Accept': 'application/json',
        'Content-type': f'multipart/form-data; boundary={boundary}'
    }

    conn.request("POST", "/v1/reports/image", body, headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    # Imprime la respuesta en el servidor para depurar
    print("Respuesta de la API:", data)

    # Devuelve la respuesta decodificada
    return data.decode("utf-8")



def historial(request):
    return render(request, 'historial.html')

def configuracion(request):
    return render(request, 'configuracion.html')