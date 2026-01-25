from django.contrib import admin
from django.db import transaction
from Usuarios.models import  Rol, Cuenta
from .models import ResultadoPorCarrera, Respuesta, Prueba, PruebaUsuario
from .services import asignar_prueba_a_aspirantes


@admin.register(ResultadoPorCarrera)
class ResultadoPorCarreraAdmin(admin.ModelAdmin):
    list_display = ('id', 'prueba_usuario', 'banco_pregunta', 'carrera_banco', "resultado_total")

    def carrera_banco(self, obj):
        return obj.banco_pregunta.carrera

@admin.register(Respuesta)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'resultado_por_carrera', 'pregunta', 'opcion')

@admin.register(PruebaUsuario)
class PruebaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'persona', 'prueba', 'estado', 'fecha_realizacion')

@admin.register(Prueba)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_inicio', 'fecha_fin', 'descripcion')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            asignar_prueba_a_aspirantes(obj)
