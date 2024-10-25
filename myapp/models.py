from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create your models here.

class Imagen(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')

    def __str__(self):
        return self.nombre
    

# Modelo para Usuarios
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Almacenamos la contraseña encriptada

    def save(self, *args, **kwargs):
        # Encriptamos la contraseña antes de guardar
        if not self.pk:  # Solo en el primer guardado
            self.password = make_password(self.password)
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    


# Este no
class Imagengeneral(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')
    tipo = models.CharField(max_length=10, choices=[('ai', 'ai'), ('human', 'human')])
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con Usuario

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"



#este tampoco
class Imagengeneralversiondos(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')
    tipo = models.CharField(max_length=10, choices=[('ai', 'IA'), ('human', 'Humano')])
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"



# Modelo para almacenar imágenes generadas por IA
class ImagenIA(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='ia/')

    def __str__(self):
        return self.nombre
    


# Modelo para almacenar imágenes humanas
class ImagenHumana(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='human/')

    def __str__(self):
        return self.nombre




class generalImagen(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')
    tipo = models.CharField(max_length=10, choices=[('ai', 'IA'), ('human', 'Humano')])

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"