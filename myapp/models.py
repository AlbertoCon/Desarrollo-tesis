from django.db import models

# Create your models here.

class Imagen(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')

    def __str__(self):
        return self.nombre