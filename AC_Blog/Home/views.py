from django.shortcuts import render
from Home import models, forms

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy

# Welcome View
def home(request):
    context = {'welcome_messege':'Bienvenido!!!.... Mi Blog!!!.'}
    return render(request, "Home/base_home.html", context)

def about(request):
    context = {'welcome_messege':'Bienvenido!!!.... Mi Blog!!!.'}
    return render(request, "Home/about.html", context)

# Class based Views
class ArtCreateView(LoginRequiredMixin, CreateView):
    model = models.Articulo
    template_name = "Home/art_create.html"
    success_url = reverse_lazy('ArtList')
    fields = ['titulo', 'subtitulo', 'contenido', 'imagen']
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class ArtDetailView(DetailView):
    model = models.Articulo
    template_name = "Home/art_detail.html"
    
class ArtUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Articulo
    template_name = "Home/art_edit.html"
    success_url = reverse_lazy('ArtList')
    fields = ['titulo', 'subtitulo', 'contenido', 'imagen']

class ArtDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Articulo
    template_name = "Home/art_delete.html"
    success_url = reverse_lazy('ArtList')

# Functions based Views
def art_list(request):
    articulos = models.Articulo.objects.all().order_by('-id')
    return render(request, 'Home/art_list.html', { 'articulos' : articulos })

def art_search_title(request):
    titulo = request.GET.get('titulo', None)
    print(titulo)
    if titulo:
        articulos = models.Articulo.objects.filter(titulo__icontains=titulo).order_by('-id')
    else:
        articulos = models.Articulo.objects.all().order_by('-id')
        
    form_search_art = forms.FormSearchArts()
    
    return render(request, 'Home/art_search_title.html', 
                  { 'form_search_art' : form_search_art, 'articulos' : articulos }
                  )

def art_list_author(request,pk):
    autor = pk
    print(autor)
    articulos = models.Articulo.objects.filter(autor=autor).order_by('-id')
    articulo = articulos[0]
    print(articulo)
    return render(request, 'Home/art_list_autor.html', { 'articulos' : articulos , 'articulo': articulo })

def my_arts(request):
    autor = request.user
    print(autor)
    articulos = models.Articulo.objects.filter(autor=autor).order_by('-id')
    return render(request, 'Home/art_list_autor.html', { 'articulos' : articulos , 'autor': autor })