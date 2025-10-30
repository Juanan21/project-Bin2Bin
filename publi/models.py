from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class categoria(models.Model):
    titulo = models.TextField(max_length=50)

    def __str__(self):
        return self.titulo

class publi(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagenes/', blank=True)
    categorias = models.ManyToManyField(categoria)

    def __str__(self):
        return self.titulo + '/' + str(self.usuario)

class Interesado(models.Model):
    publicante = models.ForeignKey(User, related_name="pub", on_delete=models.CASCADE)
    interesado = models.ForeignKey(User, related_name="inte", on_delete=models.CASCADE)
    pk_post = models.ForeignKey("publi", on_delete=models.CASCADE)

