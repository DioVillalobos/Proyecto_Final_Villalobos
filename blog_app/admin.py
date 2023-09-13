from django.contrib import admin
from .models import Page,Registrar_Usuario,Perfil_Usuario, Avatar

# Register your models here.
admin.site.site_header = "Pestaña de Administracion del Blog"

admin.site.register(Page)
admin.site.register(Registrar_Usuario)
admin.site.register(Perfil_Usuario)
admin.site.register(Avatar)