from django.test import TestCase, Client
import datetime
from datetime import date

from Home.models import Articulo
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

class VerificarRutas(TestCase):
    def test_pagina_inicio(self):
        """
        Verificar rutas
        """
        url = reverse('home')
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 200)

class EliminarArticuloTest(TestCase):
    def setUp(self):
        self.articulo = Articulo.objects.create(
            titulo = "Artículo 001", 
            subtitulo = "Artículo 001 ST", 
            contenido = "These two occurrences are not a coincidence.",
            autor_id = 1,
            # fecha_creacion = datetime.date(2024, 3, 9), # no hace falta esta definicion ya que el tag es automático en la definición del modelo
            imagen         = "",
            )
        user = get_user_model()
        user.objects.create_user('testuser', password="genericPW1788")

    def test_setup(self):
        """
        Verificar que creo adecuadamente la instancia de Articulo
        """
        hoy = date.today()
        date_year = hoy.year
        date_month = hoy.month
        date_day = hoy.day
        self.assertQuerysetEqual(Articulo.objects.filter(titulo__icontains="Artículo 001").values(), 
                                 [{'id': 1, 
                                   'titulo': 'Artículo 001', 
                                   'subtitulo': 'Artículo 001 ST', 
                                   'contenido': 'These two occurrences are not a coincidence.',
                                   'autor_id' : 1,
                                   'fecha_creacion' : datetime.date(date_year, date_month, date_day),
                                   'imagen' : "",
                                   }])
    
    def test_login(self):
        """
        Verificar que se inicie sesión
        """
        self.assertTrue(self.client.login(username='testuser', password='genericPW1788'))
    
    def test_eliminar_articulo(self):
        """
        Verificar que se elimine articulo al iniciar sesión
        """
        self.client.login(username='testuser', password='genericPW1788')
        url = reverse('ArtDelete', args=[self.articulo.id])
        respuesta = self.client.post(url)
        self.assertEqual(respuesta.status_code, 302)
        self.assertQuerysetEqual(Articulo.objects.filter(titulo__icontains="Artículo 001", subtitulo__icontains="Artículo 001 ST"), 
                                 [])

    def test_no_eliminar_estudiante(self):
        """
        Verificar que NO se elimine estudiante sin iniciar sesión
        """
        url = reverse('ArtDelete', args=[self.articulo.id])
        respuesta = self.client.post(url)
        self.assertEqual(respuesta.status_code, 302)
        hoy = date.today()
        date_year = hoy.year
        date_month = hoy.month
        date_day = hoy.day
        self.assertQuerysetEqual(Articulo.objects.filter(titulo__icontains="Artículo 001", subtitulo__icontains="Artículo 001 ST").values(), 
                                 [{'id': 1, 
                                   'titulo': 'Artículo 001', 
                                   'subtitulo': 'Artículo 001 ST', 
                                   'contenido': 'These two occurrences are not a coincidence.',
                                   'autor_id' : 1,
                                   'fecha_creacion' : datetime.date(date_year, date_month, date_day),
                                   'imagen' : "",
                                   }])
    