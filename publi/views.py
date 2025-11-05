from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .forms import publiform
from .models import publi, Interesado
from user.models import user_img
#Se llama decorador
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
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
        t.save_m2m()
        return redirect('perfil')
    
@login_required
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
                asunto = request.user.username + " se ha interesado en " + "'" + publicacion.titulo + "'"
                mensaje = "¡Hola! He visto tu publicación y me ha interesado mucho. Por favor, responde este correo para seguir en contacto. :)" \
                "\nAtentamente: " + request.user.first_name + " " + request.user.last_name
                remitente = request.user.email
                destinatario = publicacion.usuario.email
                from_email = f"Bin2Bin <miBin2Bin@gmail.com>"
                email = EmailMessage(
                    subject=asunto,
                    body=f"{mensaje}",
                    from_email=from_email,
                    to=[destinatario],
                    reply_to=[remitente],
                )
                email.send(fail_silently=False)
                return redirect(reverse('post', args=[post_id]))
    else:
        interesados = Interesado.objects.filter(pk_post_id=post_id)
        hay_interesado = Interesado.objects.filter(publicante=publicacion.usuario, interesado=request.user, pk_post=post_id).exists()
        try:
            img_obj = get_object_or_404(user_img, usuario=request.user.id)
            return render(request, 'mipubli.html', {'post':publicacion, 'interesados':interesados, 'hay_interesado':hay_interesado, 'imagen':img_obj})
        except:
            return render(request, 'mipubli.html', {'post':publicacion, 'interesados':interesados, 'hay_interesado':hay_interesado})