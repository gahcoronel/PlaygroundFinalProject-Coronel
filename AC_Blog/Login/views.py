from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from Login import forms, models
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView


# Create your views here.

def login_home(request):
    context = {'welcome_messege':'Bienvenido!!!'}
    return render(request, "Login/login.html", context)

def login_request(request):
    if request.method == 'POST':
        myform = AuthenticationForm(request, data = request.POST)
        if myform.is_valid():  # Si pasó la validación de Django
            usuario = myform.cleaned_data.get('username')
            contrasenia = myform.cleaned_data.get('password')
            user = authenticate(username = usuario, password = contrasenia)
            login(request, user)        
            return render(request, "Login/login.html", {"mensaje": f'Bienvenido {user.username}'})         
    else:
        myform = AuthenticationForm()
    return render(request, "Login/login_request.html", {"myform": myform})

def register(request):
      if request.method == 'POST':
            myform = forms.Form_Registro(request.POST)
            if myform.is_valid():
                  username = myform.cleaned_data['username']
                  myform.save()
                #   myform = AuthenticationForm()
                  return render(request,"Login/login.html" ,  {"mensaje":"Usuario Creado! Ahora ingresa."})
      else:
            myform = forms.Form_Registro()     
      return render(request,"Login/register.html" ,  {"myform":myform})

@login_required
def edit_profile(request):
    usuario = request.user
    
    if request.method == 'POST':
        myform = forms.UserEditForm(request.POST, request.FILES, instance=request.user) # forms.UserEditForm(request.POST, request.FILES, instance=request.user)
        if myform.is_valid():
            if myform.cleaned_data.get('imagen'):
                if hasattr(usuario, 'avatar'):
                    usuario.avatar.imagen = myform.cleaned_data.get('imagen')
                    usuario.avatar.save()
                else:
                    models.Avatar.objects.create(user=usuario, imagen=myform.cleaned_data.get('imagen'))
            myform.save()
            return render(request, "Login/login.html")

    else:
        myform = forms.UserEditForm(instance=request.user)
        
    return render(request, "Login/edit_profile.html", {"myform": myform, "usuario": usuario})

class change_password(LoginRequiredMixin, PasswordChangeView):
    template_name = 'Login/change_password.html'
    success_url = reverse_lazy('Login')