from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import publiform
from user.forms import modperfil
from .models import publi
from user.views import perfil
from user.models import user_img
# Create your views here.
def publi(request):
    if request.method == 'GET':
        try:
            img_obj = get_object_or_404(user_img, usuario=request.user.id)
            return render(request, 'publi.html', {
            'form': publiform, 'imagen':img_obj
            })
        except:
            return render(request, 'publi.html', {'form': publiform})
    else:
        t = publiform(request.POST)
        nueva_publi = t.save(commit=False)
        nueva_publi.usuario = request.user
        nueva_publi.save()
        return redirect('perfil')