from django.shortcuts import render
from Home import models, forms, about_info

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User


def home(request):
    articulos = models.Articulo.objects.all().order_by('-id')
    
    contexto = {}
    if len(articulos) != 0:
        contexto['articulo_1'] = articulos[0]
        contexto['articulo_2'] = articulos[1]
        contexto['articulo_3'] = articulos[2]
        contexto['articulo_4'] = articulos[3]
        contexto['articulo_5'] = articulos[4]
    
    sw_t1 = '¡Hola!'
    sw_st1 = 'Te damos la bienvenida al blog. Aquí podrás publicar artículos de tus temas favoritos.'
    contexto['sw_t1'] = sw_t1
    contexto['sw_st1'] = sw_st1
    
    return render(request, 'Home/art_welcome.html', contexto)

def about(request):
    articulo = about_info.About()
    
    sw_t1 = 'Acerca del proyecto'
    sw_st1 = 'Gracias por interesarte en mi trabajo.'
   
    return render(request, "Home/about.html", {'articulo': articulo , 'sw_t1' : sw_t1 , 'sw_st1' : sw_st1})

# Class based Views
class ArtCreateView(LoginRequiredMixin, CreateView):
    model = models.Articulo
    template_name = "Home/art_create.html"
    success_url = reverse_lazy('ArtList')
    fields = ['titulo', 'subtitulo', 'contenido', 'imagen']
    
    sw_t1 = 'Nueva publicación'
    sw_st1 = f'Completa el formulario con la información de tu nueva publicación. Recuerda que luego podrás editarla si lo deseas.' 
    extra_context={'sw_t1' : sw_t1 , 'sw_st1' : sw_st1}
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class ArtDetailView(DetailView):
    model = models.Articulo
    template_name = "Home/art_detail.html"
    
    extra_context = {}
    extra_context['sw_t1'] = 'Detalle de la publicación'
    extra_context['sw_st1'] = f'Disfruta del contenido de este artículo.'
    
class ArtUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Articulo
    template_name = "Home/art_create.html"
    success_url = reverse_lazy('home')
    fields = ['titulo', 'subtitulo', 'contenido', 'imagen']
    
    sw_t1 = 'Editar artículo'
    sw_st1 = f'Cambia en el formulario la información de tu publicación. Recuerda que luego podrás editarla nuevamente si lo deseas.' 
    extra_context={'sw_t1' : sw_t1 , 'sw_st1' : sw_st1}

class ArtDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Articulo
    template_name = "Home/art_delete.html"
    success_url = reverse_lazy('ArtList')

# Functions based Views
def art_list(request):
    articulos = models.Articulo.objects.all().order_by('-id')
    sw_t1 = 'Listado Artículos'
    sw_st1 = 'Listado de todos los artículos publicados.'
    return render(request, 'Home/art_list.html', { 'articulos' : articulos , 'sw_t1' : sw_t1 , 'sw_st1' : sw_st1})

def art_search_title(request):
    titulo = request.GET.get('titulo', None)
    if titulo:
        articulos = models.Articulo.objects.filter(titulo__icontains=titulo).order_by('-id')
    else:
        articulos = models.Articulo.objects.all().order_by('-id')
        
    form_search_art = forms.FormSearchArts()
    
    sw_t1 = '¡Hola!'
    sw_st1 = 'Te damos la bienvenida al blog. Aquí podrás publicar artículos de tus temas favoritos.'
    cantidad = len(articulos)
    
    return render(request, 'Home/art_list.html', 
                  { 'form_search_art':form_search_art , 'articulos':articulos , 'titulo':titulo , 'sw_t1' : sw_t1 , 'sw_st1' : sw_st1 , 'cantidad':cantidad}
                  )

def art_list_author(request,pk):
    autor = pk
    articulos = models.Articulo.objects.filter(autor=autor).order_by('-id')
    articulo = articulos[0]
    print(articulo)
    
    sw_t1 = 'Listado de publicaciones por autor'
    sw_st1 = f'Listado de todos los artículos publicados por: {articulo.autor}' 

    return render(request, 'Home/art_list.html', { 'articulos' : articulos , 'articulo': articulo, 'sw_t1' : sw_t1 , 'sw_st1' : sw_st1 })

def my_arts(request):
    autor = request.user
    print(autor)
    articulos = models.Articulo.objects.filter(autor=autor).order_by('-id')
    
    sw_t1 = 'Mis publicaciones'
    sw_st1 = f'Listado de todos los artículos publicados por: {autor}' 
    return render(request, 'Home/art_list.html', { 'articulos' : articulos , 'sw_t1' : sw_t1 , 'sw_st1' : sw_st1 })

def authors_list(request):
    usuarios = User.objects.all()
    autores = []
    
    for usuario in usuarios:
        autor = usuario.id
        name = usuario.username
        articulos = models.Articulo.objects.filter(autor=autor).order_by('-id')
        if articulos:
            articulo = articulos[0]
        else:
            articulo = 0
        cantidad = len(articulos)
        autores.append([name, cantidad, articulo])
    
    autores.sort(key=lambda item: item[1], reverse=True)
    
    autores_col1 = []
    autores_col2 = []
    autores_nr = len(autores)
    while autores_nr !=0:
        if autores == []:
            break
        else:
            autores_col1.append(autores.pop(0))
        if autores == []:
            break
        else:    
            autores_col2.append(autores.pop(0))
        autores_nr -= 1
    
    autores = [autores_col1, autores_col2]
    
    contexto = {}
    contexto['sw_t1'] = 'Autores'
    contexto['sw_st1'] = f'Listado de todos usuarios registrados y sus artículos publicados.'
    contexto['autores'] = autores
    
    return render(request, 'Home/author_list.html', contexto)
