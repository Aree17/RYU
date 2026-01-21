from django import forms
from django.contrib.auth.models import User
from .models import Persona, Cuenta

class RegistroForm(forms.Form):
    username = forms.CharField(max_length=150)
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    correo = forms.EmailField()
    cedula = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

