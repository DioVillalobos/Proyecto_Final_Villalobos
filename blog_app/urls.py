from django.urls import path
from.views import *
from django.contrib.auth.views import LogoutView,LoginView

urlpatterns = [
    path('registrar_usuario/', registrar_usuario, name='registrar_usuario'), #tomar esto como ejemplo para el resto de Urls
    path('perfil_usuario/', perfil_usuario, name='perfil_usuario'),
    path('blog/', blog, name='blog'),
    path('listar_blog/', listar_blog, name='listar_blog'),
    path('crear_blog/', crear_blog, name='crear_blog'),
    path('busqueda_temas_blog/', busqueda_temas_blog, name='busqueda_temas_blog'),
    path('buscar_tema/', buscar_tema, name='buscar_tema'),
    path("eliminar_usuario/<id>", eliminar_usuario, name="eliminar_usuario"),
    path('editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),
    path('inicio_sesion/', mi_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
]