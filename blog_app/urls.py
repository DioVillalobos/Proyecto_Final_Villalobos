from django.urls import path, include
from . import views
from .views import *
from django.contrib.auth.views import LogoutView,LoginView

urlpatterns = [
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('page/<int:page_id>/', views.page, name='page'),
    path('blog_app/page/<int:page_id>/', views.page_view, name='page_with_id'),
    path('crear_blog/', views.crear_blog, name='crear_blog'),
    path('busqueda_temas_blog/', views.busqueda_temas_blog, name='busqueda_temas_blog'),
    path('buscar_tema/', views.buscar_tema, name='buscar_tema'),
    path('eliminar_perfil/', views.eliminar_perfil, name='eliminar_perfil'),
    path('inicio_sesion/', views.mi_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('about/', views.about, name='about'),
    path('detalle_blog/<int:page_id>/', views.detalle_blog, name='detalle_blog'),
     path('messages_app/', include('messages_app.urls')),  
]