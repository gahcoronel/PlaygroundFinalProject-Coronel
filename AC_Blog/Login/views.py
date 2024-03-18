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
            
            sw_t1 = f'¡Hola {user.username}!'
            sw_st1 = f'Te damos la bienvenida al blog. Aquí podrás publicar artículos de tus temas favoritos.' 
        
            return render(request, "Home/art_welcome.html", {'sw_t1':sw_t1 , 'sw_st1':sw_st1})
    else:
        myform = AuthenticationForm()
        
    sw_t1 = 'Ingresar'
    sw_st1 = f'Ingresa tu nombre de usuario y contraseña.'   
        
    return render(request, "Login/login_request.html", {"myform": myform , 'sw_t1':sw_t1 , 'sw_st1':sw_st1})

def register(request):
    if request.method == 'POST':
        myform = forms.Form_Registro(request.POST)
        if myform.is_valid():
            username = myform.cleaned_data['username']
            myform.save()
            myform = AuthenticationForm()
            
            sw_t1 = 'Ingresar'
            sw_st1 = f'¡Registro exitoso! Ahora ingresa con tu usuario y contraseña.'
            
            return render(request, "Home/art_welcome.html", {"myform": myform , 'sw_t1':sw_t1 , 'sw_st1':sw_st1})
    else:
        myform = forms.Form_Registro()   
            
    sw_t1 = 'Registrarse'
    sw_st1 = f'Ingresa un nombre de usuario y tu contraseña.' 
    return render(request,"Login/register.html" ,  {"myform": myform , 'sw_t1':sw_t1 , 'sw_st1':sw_st1})

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
            return render(request, "Login/detail_profile.html")

    else:
        myform = forms.UserEditForm(instance=request.user)
        
        sw_t1 = 'Editar Perfil'
        sw_st1 = f'Complete o edite su información de usuario, o combie su contraseña' 
        
    return render(request, "Login/edit_profile.html", {"myform": myform , 'sw_t1':sw_t1 , 'sw_st1':sw_st1})

class change_password(LoginRequiredMixin, PasswordChangeView):
    template_name = 'Login/change_password.html'
    success_url = reverse_lazy('Detail_Profile')
    
@login_required
def detail_profile(request):
    sw_t1 = 'Datos de Perfil'
    sw_st1 = f'Aquí puedes modificar tus datos de usuario.' 
        
    return render(request, "Login/detail_profile.html", {'sw_t1':sw_t1 , 'sw_st1':sw_st1})