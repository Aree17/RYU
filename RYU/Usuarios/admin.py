from django.contrib import admin
from .models import Persona, Cuenta


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "correo", "cedula")
    search_fields = ("nombres", "apellidos", "correo", "cedula")
    list_filter = ("correo",)
    ordering = ("apellidos", "nombres")


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ("get_usuario", "rol", "activo")
    ordering = ("usuario__username",)

    def get_usuario(self, obj):
        return obj.user.username

    get_usuario.short_description = "Usuario"