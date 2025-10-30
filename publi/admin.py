from django.contrib import admin
from .models import publi, Interesado, categoria

class adminpubli(admin.ModelAdmin):
    readonly_fields = ('creacion', )
    
# Register your models here.
admin.site.register(publi, adminpubli)
admin.site.register(Interesado)
admin.site.register(categoria)