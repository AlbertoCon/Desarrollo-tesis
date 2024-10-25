from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont


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



# Modelo para almacenar imágenes generadas por IA, este ya no
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
    


# Modelo para imágenes generadas por IA
class iaimagen(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='ia/')

    def __str__(self):
        return self.nombre

    def marcar_imagen(self):
        """Agrega un sello que diga 'Hecho por una IA'."""
        with Image.open(self.imagen.path) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()  # Usa la fuente predeterminada

            # Define la posición del texto y color
            text = "Hecho por una IA"
            text_width, text_height = draw.textsize(text, font=font)
            position = (img.width - text_width - 10, img.height - text_height - 10)

            # Dibuja el texto en la imagen
            draw.text(position, text, (255, 0, 0), font=font)

            # Guarda la imagen modificada
            img.save(self.imagen.path)



class iaimagenverdos(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='ia/')

    def __str__(self):
        return self.nombre

    def marcar_imagen(self):
        """Agrega un sello que diga 'Hecho por una IA'."""
        with Image.open(self.imagen.path) as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()  # Usa la fuente predeterminada

            # Define el texto y su color
            text = "Hecho por una IA"

            # Obtén las dimensiones del texto utilizando textbbox()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

            # Define la posición en la esquina inferior derecha
            position = (img.width - text_width - 10, img.height - text_height - 10)

            # Dibuja el texto en la imagen
            draw.text(position, text, fill=(255, 0, 0), font=font)

            # Guarda la imagen modificada
            img.save(self.imagen.path)