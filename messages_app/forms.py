from django import forms
from django.contrib.auth.models import User

class NuevoMensajeForm(forms.Form):
    destinatario = forms.ModelChoiceField(queryset=User.objects.all(), label='Selecciona un destinatario')
    contenido = forms.CharField(widget=forms.Textarea, label='Mensaje')