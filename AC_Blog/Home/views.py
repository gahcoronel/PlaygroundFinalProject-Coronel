from django.shortcuts import render
from Home import models, forms, about_info

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy


def home(request):
    articulos = models.Articulo.objects.all().order_by('-id')
    print(len(articulos))
    
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
    
    sw_t1 = 'Detalle de la publicación'
    sw_st1 = f'Disfruta del contenido de este artículo.' 
    extra_context={'sw_t1' : sw_t1 , 'sw_st1' : sw_st1}
    
class ArtUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Articulo
    template_name = "Home/art_create.html"
    success_url = reverse_lazy('ArtDetail')
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
    print(titulo)
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
    print(autor)
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