from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import publiform
from user.forms import modperfil
from .models import publi, Interesado
from user.views import perfil
from user.models import user_img
# Create your views here.
def publis(request):
    if request.method == 'GET':
        try:
            img_obj = get_object_or_404(user_img, usuario=request.user.id)
            return render(request, 'publi.html', {
            'form': publiform, 'imagen':img_obj
            })
        except:
            return render(request, 'publi.html', {'form': publiform})
    else:
        t = publiform(request.POST, request.FILES)
        nueva_publi = t.save(commit=False)
        nueva_publi.usuario = request.user
        nueva_publi.save()
        return redirect('perfil')
    
def post(request, post_id):
    publicacion = get_object_or_404(publi, id=post_id)
    if request.method == 'POST':
        usuario1 = request.user.id
        usuario2 = publicacion.usuario.id
        if usuario1 == usuario2:
            publicacion.delete()
            return redirect('perfil')
        else:
            hay_interesado = Interesado.objects.filter(publicante=publicacion.usuario, interesado=request.user, pk_post=post_id).exists()
            if hay_interesado == True:  
                el_interesado = get_object_or_404(Interesado, publicante=publicacion.usuario, interesado=request.user, pk_post=post_id)
                el_interesado.delete()
                return redirect(reverse('post', args=[post_id]))
            else:
                Interesado.objects.create(publicante_id=usuario2, interesado_id=usuario1, pk_post_id=post_id)
                return redirect(reverse('post', args=[post_id]))
    else:
        interesados = Interesado.objects.filter(pk_post_id=post_id)
        hay_interesado = Interesado.objects.filter(publicante=publicacion.usuario, interesado=request.user, pk_post=post_id).exists()
        try:
            img_obj = get_object_or_404(user_img, usuario=request.user.id)
            return render(request, 'mipubli.html', {'post':publicacion, 'interesados':interesados, 'hay_interesado':hay_interesado, 'imagen':img_obj})
        except:
            return render(request, 'mipubli.html', {'post':publicacion, 'interesados':interesados, 'hay_interesado':hay_interesado})