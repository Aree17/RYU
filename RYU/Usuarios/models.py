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
    # Relación 1 a 1 (cada Persona tiene exactamente una Cuenta y viceversa)
    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name="cuenta"
    )

    usuario = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=128, verbose_name="contraseña")
    activo = models.BooleanField(default=True)

    # Rol (enumeración del diagrama)
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ASPIRANTE
    )

    def __str__(self):
        return f"{self.usuario} - {self.rol}"
