from django.contrib.auth.models import User
from django.db import models


class Rol(models.TextChoices):
    ADMINISTRADOR = "ADMINISTRADOR", "ADMINISTRADOR"
    ASPIRANTE = "ASPIRANTE", "ASPIRANTE"


class Persona(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    cedula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.cedula})"


class Cuenta(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    activo = models.BooleanField(default=True)

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ASPIRANTE
    )

    def __str__(self):
        return self.user.username