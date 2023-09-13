from django.db import models
from django.contrib.auth.models import User

class Conversacion(models.Model):
    usuario_origen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversaciones_origen')
    usuario_destino = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversaciones_destino')

    def __str__(self):
        return f"Conversación entre {self.usuario_origen} y {self.usuario_destino}"

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    remitente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.remitente} en {self.conversacion}"