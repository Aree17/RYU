from django.contrib import admin

from .models import ResultadoPorCarrera, Resultado, Prueba

@admin.register(ResultadoPorCarrera)
class ResultadoPorCarreraAdmin(admin.ModelAdmin):
    list_display = ('id', 'prueba', 'banco_pregunta')


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'resultado_por_carrera', 'pregunta_opcion')


@admin.register(Prueba)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_realizacion', 'persona', 'periodo_academico')