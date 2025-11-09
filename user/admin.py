from django.contrib import admin
from .models import user_img, Descripcion

class adminpubli(admin.ModelAdmin):
    readonly_fields = ('creacion', )

# Register your models here.
admin.site.register(user_img)
admin.site.register(Descripcion)
