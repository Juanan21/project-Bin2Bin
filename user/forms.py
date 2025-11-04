from django.forms import ModelForm
from .models import user_img
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class first_lastn(ModelForm):
    nombre = forms.CharField(max_length=30, required=True)
    apellido = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=60, required=True)
    username = forms.CharField(max_length=30, required = True)
    password1= forms.CharField(max_length=60, required = True)
    password2= forms.CharField(max_length=60, required = True)
    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellido', 'email', 'password1', 'password2']

class modperfil(ModelForm):
    class Meta:
        model = User
        fields = ['email']

class imgperfil(ModelForm):
    class Meta:
        model = user_img
        fields = ['imagen']