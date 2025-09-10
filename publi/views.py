from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import publiform
from user.forms import modperfil
from .models import publi
from user.views import perfil
# Create your views here.
def publi(request):
    if request.method == 'GET':
        return render(request, 'publi.html', {
            'form': publiform
        })
    else:
        t = publiform(request.POST)
        nueva_publi = t.save(commit=False)
        nueva_publi.usuario = request.user
        nueva_publi.save()
        return perfil(request)