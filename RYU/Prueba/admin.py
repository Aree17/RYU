from django.contrib import admin
from .models import (
Pregunta, BancoPreguntas, Opcion
)
# Register your models here.
@admin.register(BancoPreguntas)
class BancoPreguntasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'carrera', 'periodos', 'vigente')
    list_filter = ('periodoVigente', 'carrera',)
    search_fields = ('banco_preguntas',)

    def periodos(self, obj):
        return ", ".join(p.nombre for p in obj.periodoVigente.all())

    periodos.short_description = "Períodos"

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('enunciado', 'banco','pregunta_opcion')


    def pregunta_opcion(self, obj):
        return ", ".join(p.contenido for p in obj.opcion.all())
    pregunta_opcion.short_description = "Opcion"

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'valor')
    list_filter = ('contenido','valor')