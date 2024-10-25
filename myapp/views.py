from django.shortcuts import render, redirect
from .forms import ImagenForm
from django.http import JsonResponse

# Create your views here.


def cargar_imagen(request):
    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cargar_imagen')
    else:
        form = ImagenForm()
    return render(request, 'cargar_imagen.html', {'form': form})

