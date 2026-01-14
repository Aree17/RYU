from django.contrib import admin
from .models import (
    BancoPregunta, Pregunta, Opcion, PreguntaOpcion
)
# Register your models here.
@admin.register(BancoPregunta)
class BancoPreguntaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'vigente',)
    list_filter = ('vigente',)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'banco_pregunta')
    list_filter = ('enunciado','banco_pregunta',)

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'valor',)
    list_filter = ('contenido', 'valor',)
    search_fields = ('valor',)

@admin.register(PreguntaOpcion)
class PreguntaOpcionAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'opcion',)
    list_filter = ('pregunta', 'opcion',)
    search_fields = ('pregunta__enunciado',)