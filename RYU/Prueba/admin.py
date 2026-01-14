from django.contrib import admin
from .models import (
Pregunta, BancoPregunta, Opcion, PreguntaOpcion
)
# Register your models here.
@admin.register(BancoPregunta)
class BancoPreguntaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'vigente', 'periodoVigente', 'carrera')
    list_filter = ('vigente','periodoVigente', 'carrera')
    search_fields = ('BancoPreguntas__enunciado',)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'banco')
    list_filter = ('banco',)

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'valor')
    list_filter = ('contenido','valor')

@admin.register(PreguntaOpcion)
class PreguntaOpcionAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'opcion')
    list_filter = ('pregunta',)
    search_fields = ('pregunta__enunciado',)

