from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Page, UserProfile

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['nombre_page','tema_page','contenido_page','imagen_page']

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
        help_texts = {k: "" for k in fields}

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['description', 'profile_picture']

    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'rows': 3}))
    profile_picture = forms.ImageField()