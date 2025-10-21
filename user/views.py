from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import first_lastn, modperfil, imgperfil
from .models import user_img
from publi.models import publi
# Create your views here.

def hola(request):
    if request.method == 'POST':
        logout(request)
        return redirect('hola')
    else:
        try:
            publicaciones = publi.objects.filter(titulo__contains=request.GET["search"]).order_by("-creacion")
            try:
                img_obj = get_object_or_404(user_img, usuario=request.user.id)
                return render(request, 'hola.html', {'imagen':img_obj, 'publicaciones':publicaciones})
            except:
                return render(request, 'hola.html', {'publicaciones':publicaciones})
        except:
            publicaciones = publi.objects.all().order_by("-creacion")
            try:
                img_obj = get_object_or_404(user_img, usuario=request.user.id)
                return render(request, 'hola.html', {'imagen':img_obj, 'publicaciones':publicaciones})
            except:
                return render(request, 'hola.html', {'publicaciones':publicaciones})

def signup(request):
    if request.method == 'GET':
        titulo = 'Hola, bienvenido. Crea una cuenta'
        cuerpo = 'mucho gusto'
        return render(request, 'signup.html', {
            'titulo':titulo,
            'cuerpo':cuerpo,
            'form':first_lastn,
            'form1':imgperfil
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #first_last = first_lastn(request.POST)
                usuario = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], first_name=request.POST['nombre'], last_name=request.POST['apellido'], email=request.POST['email'])
                imagen_form = imgperfil(request.POST, request.FILES)
                usuario.save()
                login(request, usuario)
                if imagen_form.is_valid():
                    imagen = imagen_form.save(commit=False)
                    imagen.usuario = usuario 
                    imagen.save()
                print(request.POST)
                return redirect('perfil')
            except:
                titulo = 'Nombre de usuario ya existente. Intente con otro'
            return render(request, 'signup.html', {
                'titulo':titulo,
                'form':first_lastn,
                'form1':imgperfil
            })
        else:
            titulo = 'Las contraseñas no coinciden'
            return render(request, 'signup.html', {
                'titulo':titulo,
                'form':first_lastn,
                'form1':imgperfil
            })

def perfil(request):
    if request.method == 'POST':
        img_obj = get_object_or_404(user_img, usuario=request.user.id)
        imagen = imgperfil(request.POST, request.FILES, instance=img_obj)
        if imagen.is_valid():
            imagen.save()
        if "update_email" in request.POST:
            mod = modperfil(request.POST, instance=request.user)
            if mod.is_valid():
                mod.save()
            else:
                return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'imagen':imagen, 'error':'email invalido'})
        return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'imagen':imagen})
    else:
        try:
            img_obj = get_object_or_404(user_img, usuario=request.user.id)
            try:
                publicaciones = publi.objects.filter(usuario=request.user.id).order_by("-creacion")
                return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'imagen':img_obj, 'publicaciones':publicaciones})
            except:
                print(img_obj)
                return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'imagen':img_obj})
        except:
            return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil})
    
def signin(request):
    if request.method == 'GET':    
        return render(request, 'signin.html', {
            'form':AuthenticationForm
        })  
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form':AuthenticationForm,
                'error': 'Nombre de usuario o contraseña incorrecto'
            })  
        else:
            login(request, user)
            return redirect('perfil')
        
def log(request):
    try:
        img_obj = get_object_or_404(user_img, usuario=request.user.id)
        return render(request, 'logout.html', {'imagen':img_obj})
    except:
        return render(request, 'logout.html')

    