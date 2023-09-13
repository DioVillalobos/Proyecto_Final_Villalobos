from django.urls import path
from . import views

urlpatterns = [
    path('lista-conversaciones/', views.lista_conversaciones, name='lista_conversaciones'),
    path('ver_conversacion/<int:conversacion_id>/', views.ver_conversacion, name='ver_conversacion'),
    path('enviar_mensaje/<int:conversacion_id>/', views.enviar_mensaje, name='enviar_mensaje'),
    path('nueva_conversacion/', views.nueva_conversacion, name='nueva_conversacion'),
    path('crear_conversacion/<int:usuario_destino_id>/', views.crear_conversacion, name='crear_conversacion'),
]