from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Articulo(models.Model):

    titulo         = models.CharField(max_length=255)
    subtitulo      = models.CharField(max_length=255)
    contenido      = models.TextField(null=True)
    autor          = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateField(auto_now_add=True, auto_now=False)
    imagen         = models.ImageField(upload_to='postales', null=True, blank=True)
    
    def __str__(self):
        return f"[{self.id}] {self.titulo} --- {self.autor} --- {self.fecha_creacion} --- {self.imagen}"
