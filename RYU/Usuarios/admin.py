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
    list_display = ("usuario", "rol", "activo", "persona")
    search_fields = ("usuario", "persona__nombres", "persona__apellidos", "persona__cedula", "persona__correo")
    list_filter = ("rol", "activo")
    ordering = ("usuario",)
