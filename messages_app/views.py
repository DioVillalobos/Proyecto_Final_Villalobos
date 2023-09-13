from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Conversacion, Mensaje
from django.contrib.auth.models import User
from .forms import NuevoMensajeForm

@login_required
def lista_conversaciones(request):
    conversaciones = Conversacion.objects.filter(usuario_origen=request.user) | Conversacion.objects.filter(usuario_destino=request.user)
    if not conversaciones:
        return redirect('nueva_conversacion')
    return render(request, 'messages/lista_conversaciones.html', {'conversaciones': conversaciones})

@login_required
def ver_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, pk=conversacion_id)
    if conversacion.usuario_origen == request.user or conversacion.usuario_destino == request.user:
        mensajes = Mensaje.objects.filter(conversacion=conversacion)
        return render(request, 'messages/ver_conversacion.html', {'conversacion': conversacion, 'mensajes': mensajes})
    else:
        return redirect('lista_conversaciones')

@login_required
def enviar_mensaje(request, conversacion_id):
    conversacion = get_object_or_404(Conversacion, pk=conversacion_id)
    if conversacion.usuario_origen == request.user or conversacion.usuario_destino == request.user:
        if request.method == 'POST':
            contenido = request.POST['contenido']
            mensaje = Mensaje(conversacion=conversacion, remitente=request.user, contenido=contenido)
            mensaje.save()
    return redirect('ver_conversacion', conversacion_id=conversacion_id)

@login_required
def nueva_conversacion(request):
    if request.method == 'POST':
        destinatario_id = request.POST.get('destinatario')
        contenido = request.POST.get('contenido')
        if destinatario_id and contenido:
            destinatario = User.objects.get(pk=destinatario_id)
            conversacion_existente = Conversacion.objects.filter(
                usuario_origen=request.user,
                usuario_destino=destinatario
            ).first()
            if conversacion_existente:
                return redirect('ver_conversacion', conversacion_id=conversacion_existente.id)
            else:
                conversacion = Conversacion(usuario_origen=request.user, usuario_destino=destinatario)
                conversacion.save()
                mensaje = Mensaje(conversacion=conversacion, remitente=request.user, contenido=contenido)
                mensaje.save()
                return redirect('ver_conversacion', conversacion_id=conversacion.id)
    usuarios = User.objects.exclude(username=request.user.username)
    return render(request, 'messages/nueva_conversacion.html', {'usuarios': usuarios})

@login_required
def crear_conversacion(request, usuario_destino_id):
    usuario_destino = get_object_or_404(User, pk=usuario_destino_id)
    if request.user != usuario_destino:  
        conversacion_existente = Conversacion.objects.filter(
            usuario_origen=request.user,
            usuario_destino=usuario_destino
        ).first()
        if conversacion_existente:
            return redirect('ver_conversacion', conversacion_id=conversacion_existente.id)
        else:
            conversacion = Conversacion(usuario_origen=request.user, usuario_destino=usuario_destino)
            conversacion.save()
            return redirect('ver_conversacion', conversacion_id=conversacion.id)
    else:
        return redirect('nueva_conversacion')