from django.db import models   #NO OLVIDAR AGREGAR LOS MODELS EN EL APARTADO ADMIN.PY
from django.contrib.auth.models import User

class Blog(models.Model):
    nombre_blog=models.CharField(max_length=50)
    tema_blog=models.CharField(max_length=50)
    def __str__(self):         #Esto permite imprimir en el panel de /admin la info de manera correcta.
        return f"{self.nombre_blog} - {self.tema_blog}"

class Registrar_Usuario(models.Model):
    nombre_usuario=models.CharField(max_length=50)
    contraseña_usuario=models.CharField(max_length=50)
    email_usuario=models.EmailField()
    class Meta:
        verbose_name_plural = "Usuarios Registrados"  #Cambiar como se muestra en el /admin
    def __str__(self):
        return f"{self.nombre_usuario} - {self.contraseña_usuario} - {self.email_usuario}"
    

class Perfil_Usuario(models.Model):
    nombre_usuario_registrado=models.CharField(max_length=50)
    
class Avatar(models.Model):
    img= models.ImageField(upload_to="avatars")
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)