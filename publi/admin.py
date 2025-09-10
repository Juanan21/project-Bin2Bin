from django.contrib import admin
from .models import publi

class adminpubli(admin.ModelAdmin):
    readonly_fields = ('creacion', )
    
# Register your models here.
admin.site.register(publi, adminpubli)
