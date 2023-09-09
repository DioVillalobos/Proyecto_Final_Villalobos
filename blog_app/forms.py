from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BlogForm(forms.Form):
    nombre_blog=forms.CharField(max_length=50)
    tema_blog=forms.CharField(max_length=50)

class RegistrarUsuarioForm(forms.Form):
    nombre_usuario = forms.CharField(max_length=50)
    contraseña_usuario = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email_usuario = forms.EmailField()
   
class RegistroUsuarioForm(UserCreationForm):
    email=forms.EmailField(label="Email")
    password1=forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["username", "email", "password1", "password2"]
        help_texts = {k:"" for k in fields}

class UserEditorForm(UserCreationForm):
    email=forms.EmailField(label="Modificar Email")
    password1=forms.CharField(label="Modificar Contraseña", widget=forms.PasswordInput)
    password2=forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput)
    first_name=forms.CharField(label="Editar Nombre")
    last_name=forms.CharField(label="Editar Apellido")
    class Meta:
        model=User
        fields=["username", "email", "password1", "password2"]
        help_texts = {k:"" for k in fields}