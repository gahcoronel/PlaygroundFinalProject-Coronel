from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class Form_Registro(UserCreationForm):
    username = forms.TextInput()
    # email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
    
class UserEditForm(UserChangeForm):
    password = None
    email = forms.EmailField(label="email", required=False)
    last_name = forms.CharField(label='Apellido')
    first_name = forms.CharField(label='Nombre')
    imagen = forms.ImageField(label="Avatar", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'imagen']