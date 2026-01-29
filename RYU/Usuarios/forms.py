from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from Usuarios.models import Persona


class RegistroForm(forms.Form):
    username = forms.CharField(max_length=150)
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    correo = forms.EmailField()

    cedula = forms.CharField(
        max_length=10,
        min_length=10,
        help_text="La cédula debe tener exactamente 10 dígitos numéricos."
    )

    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text=(
            "<ul>"
            "<li>La contraseña debe tener al menos 8 caracteres.</li>"
            "<li>No debe ser una contraseña común.</li>"
            "<li>No puede ser completamente numérica.</li>"
            "</ul>"
        )
    )

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()

        if not username:
            raise forms.ValidationError("El usuario es obligatorio.")

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("El usuario ya existe.")

        return username

    def clean_correo(self):
        correo = (self.cleaned_data.get("correo") or "").strip()

        if not correo:
            raise forms.ValidationError("El correo es obligatorio.")

        if Persona.objects.filter(correo__iexact=correo).exists():
            raise forms.ValidationError("Este correo ya fue registrado.")

        return correo

    def clean_cedula(self):
        cedula = (self.cleaned_data.get("cedula") or "").strip()

        if not cedula:
            raise forms.ValidationError("La cédula es obligatoria.")

        if not cedula.isdigit():
            raise forms.ValidationError("La cédula debe contener únicamente números.")

        if len(cedula) != 10:
            raise forms.ValidationError("La cédula debe tener exactamente 10 dígitos.")

        if Persona.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError("Esta cédula ya fue registrada.")

        return cedula

    def clean_password(self):
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")

        user = User(username=username)

        try:
            validate_password(password, user)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)

        return password
