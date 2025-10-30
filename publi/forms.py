from django.forms import ModelForm
from .models import publi
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class publiform(ModelForm):
    class Meta:
        model = publi
        fields = ['titulo', 'descripcion', 'imagen', 'categorias']