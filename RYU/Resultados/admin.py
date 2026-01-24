from django.contrib import admin

from .models import ResultadoPorCarrera, Respuesta, Prueba, PruebaUsuario


@admin.register(ResultadoPorCarrera)
class ResultadoPorCarreraAdmin(admin.ModelAdmin):
    list_display = ('id', 'prueba', 'banco_pregunta')


@admin.register(Respuesta)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'resultado_por_carrera', 'pregunta_opcion')

@admin.register(PruebaUsuario)
class PruebaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'persona', 'prueba', 'estado', 'fecha_realizacion')


@admin.register(Prueba)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_inicio', 'fecha_fin', 'descripcion')