from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class user_img(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.usuario)
    
class Descripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.TextField(default='Descripción', blank=True)

    def __str__(self):
        return str(self.usuario)