from django.contrib.auth.models import User
from django.db import models


class Page(models.Model):                 # corresponde a los BLOGS (AYUDA)
    nombre_page=models.CharField(max_length=150)
    tema_page=models.CharField(max_length=150)
    contenido_page=models.TextField()
    autor_page=models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_page=models.DateTimeField(auto_now_add=True)
    imagen_page=models.ImageField(upload_to='page_images')

    def __str__(self):         #Esto permite imprimir en el panel de /admin la info de manera correcta.
        return f"{self.nombre_page} - {self.tema_page} - {self.autor_page}"

class Registrar_Usuario(models.Model):
    nombre_usuario=models.CharField(max_length=50)
    contraseña_usuario=models.CharField(max_length=50)
    email_usuario=models.EmailField()
    class Meta:
        verbose_name_plural = "Usuarios Registrados"  #Cambiar como se muestra en el /admin
    def __str__(self):
        return f"{self.nombre_usuario} - {self.contraseña_usuario} - {self.email_usuario}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures", blank=True)

    def __str__(self):
        return self.user.username
    
class Avatar(models.Model):
    img= models.ImageField(upload_to="avatars")
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Perfil_Usuario(models.Model):
    nombre_usuario_registrado = models.CharField(max_length=50)
    # Otros campos relacionados con el perfil del usuario

    def __str__(self):
        return self.nombre_usuario_registrado