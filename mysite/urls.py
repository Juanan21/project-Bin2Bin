"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from publi import views as publi_views
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hola, name = 'hola'),
    path('signup/', views.signup, name = 'signup'),
    path('perfil/', views.perfil, name = 'perfil'),
    path('signin/', views.signin, name = 'signin'),
    path('logout/', views.log, name = 'logout'),
    path('publicar/', publi_views.publis, name = 'publi'),
    path('imagen/<int:imagen_id>/editar/', views.imgperfil, name='img_perfil'),
    path('perfil/post/<int:id>/', publi_views.post, name='post')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
