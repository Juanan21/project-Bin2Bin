from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import first_lastn, modperfil, imgperfil, EmailForm, DescripcionForm, ModDescripcion
from .models import user_img, Descripcion
from publi.models import publi,categoria
from django.core.mail import send_mail, EmailMessage
# Create your views here.

def hola(request):
    if request.method == 'POST':
        logout(request)
        return redirect('hola')
    else:
        categorias = categoria.objects.all().order_by("titulo")
        filtros = {}
        if request.GET.get("categoria"):
            filtros['categorias__id'] = request.GET.get("categoria")
        if request.GET.get("search"):
            filtros['titulo__contains'] = request.GET.get("search")
        if filtros:
            publicaciones = publi.objects.filter(**filtros).order_by("-creacion")            
        else:
            publicaciones = publi.objects.all().order_by("-creacion")            
        try:
            img_obj = get_object_or_404(user_img, usuario=request.user.id)
            return render(request, 'hola.html', {'imagen':img_obj, 'publicaciones':publicaciones, 'categorias':categorias})
        except:
            return render(request, 'hola.html', {'publicaciones':publicaciones, 'categorias':categorias})

def signup(request):
    if request.method == 'GET':
        titulo = 'Hola, bienvenido. Crea una cuenta'
        cuerpo = 'mucho gusto'
        return render(request, 'signup.html', {
            'titulo':titulo,
            'cuerpo':cuerpo,
            'form':first_lastn,
            'form1':imgperfil,
            'form2':DescripcionForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], first_name=request.POST['nombre'], last_name=request.POST['apellido'], email=request.POST['email'])
                imagen_form = imgperfil(request.POST, request.FILES)
                descripcion_form = DescripcionForm(request.POST)
                print(descripcion_form)
                usuario.save()
                login(request, usuario)
                if imagen_form.is_valid():
                    imagen = imagen_form.save(commit=False)
                    imagen.usuario = usuario 
                    imagen.save()
                    if descripcion_form.is_valid():
                        print(hola)
                        descripcion = descripcion_form.save(commit=False)
                        descripcion.usuario = usuario
                        descripcion.save()
                        return redirect('perfil')
                    return redirect('perfil')
            except:
                titulo = 'Nombre de usuario ya existente. Intente con otro'
            return render(request, 'signup.html', {
                'titulo':titulo,
                'form':first_lastn,
                'form1':imgperfil,
                'form2':DescripcionForm
            })
        else:
            titulo = 'Las contraseñas no coinciden'
            return render(request, 'signup.html', {
                'titulo':titulo,
                'form':first_lastn,
                'form1':imgperfil,
                'form2':DescripcionForm
            })

def perfil(request):
    if request.method == 'POST':
        img_obj = get_object_or_404(user_img, usuario=request.user.id)
        imagen = imgperfil(request.POST, request.FILES, instance=img_obj)
        descripcion = Descripcion.objects.get(usuario=request.user.id)
        if imagen.is_valid():
            imagen.save()
        if "update_email" in request.POST:
            mod = modperfil(request.POST, instance=request.user)
            if mod.is_valid():
                mod.save()
            else:
                return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'form2':ModDescripcion, 'imagen':imagen, 'error':'email invalido'})
        if "update_descripcion" in request.POST:
            print('hola')
            mod = ModDescripcion(request.POST, instance=descripcion)
            if mod.is_valid():
                mod.save()
            else:
                return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'form2':ModDescripcion, 'imagen':imagen, 'error':'email invalido'})    
        return redirect('perfil')
    else:
        try:
            img_obj = get_object_or_404(user_img, usuario=request.user)
            descrip = Descripcion.objects.get(usuario=request.user.id)
            try:
                mod = ModDescripcion(instance=descrip)
                publicaciones = publi.objects.filter(usuario=request.user.id).order_by("-creacion")
                publis_interesado = publi.objects.filter(interesado__interesado_id=request.user.id).distinct()

                return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'form2':mod, 'imagen':img_obj,
                                                       'publicaciones':publicaciones, 
                                                       'descrip':descrip,
                                                       'publis_interesado':publis_interesado})
            except:
                return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'form2':mod, 'imagen':img_obj, 'descrip':descrip})
        except:
            return render(request,'perfil.html', {'form':modperfil, 'form1':imgperfil, 'form2':mod})
        
def verperfil(request, username):
    if request.method == 'GET':
        interesado = get_object_or_404(User, username=username)
        img_obj = get_object_or_404(user_img, usuario=request.user.id)
        img_inte = get_object_or_404(user_img, usuario=interesado.id)
        descrip_obj = get_object_or_404(Descripcion, usuario=interesado.id)
        publicaciones = publi.objects.filter(usuario=interesado).order_by("-creacion")
        return render(request,'verperfil.html', {'imagen':img_obj, 'publicaciones':publicaciones, 'img_inte':img_inte, 'descrip_obj':descrip_obj, 'interesado':interesado, 'form':EmailForm})
    else:
        form = EmailForm(request.POST)
        if form.is_valid():
            interesado = get_object_or_404(User, username=username)
            asunto = request.user.username + " te ha enviado un mensaje"
            mensaje = form.cleaned_data['mensaje']
            remitente = request.user.email
            destinatario = interesado.email
            from_email = f"Bin2Bin <miBin2Bin@gmail.com>"
            email = EmailMessage(
                        subject=asunto,
                        body=f"{mensaje}",
                        from_email=from_email,
                        to=[destinatario],
                        reply_to=[remitente],
                    )
            email.send(fail_silently=False)
            return redirect(reverse('ver_perfil', args=[username]))
        else:
            return redirect(reverse('ver_perfil', args=[username]))
    
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

    