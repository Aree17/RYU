from django.contrib import admin
from .models import (
Pregunta, BancoPreguntas, Opcion
)
# Register your models here.
@admin.register(BancoPreguntas)
class BancoPreguntasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'carrera', 'periodos', 'vigente')
    list_filter = ('periodoVigente', 'carrera',)
    search_fields = ('nombre',)

    def periodos(self, obj):
        return ", ".join(p.nombre for p in obj.periodoVigente.all())

    periodos.short_description = "Períodos"

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'banco')
    search_fields = ('enunciado',)
    list_filter = ('banco',)

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'valor')
    search_fields = ('contenido',)
    list_filter = ('valor',)