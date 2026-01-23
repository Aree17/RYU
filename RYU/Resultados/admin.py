from django.contrib import admin
from django.db import transaction
from Usuarios.models import  Rol, Cuenta
from .models import ResultadoPorCarrera, Respuesta, Prueba, PruebaUsuario


@admin.register(ResultadoPorCarrera)
class ResultadoPorCarreraAdmin(admin.ModelAdmin):
    list_display = ('id', 'prueba', 'banco_pregunta')


@admin.register(Respuesta)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'resultado_por_carrera', 'pregunta', 'opcion')

@admin.register(PruebaUsuario)
class PruebaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'persona', 'prueba', 'estado', 'fecha_realizacion')

@admin.register(Prueba)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_inicio', 'fecha_fin', 'descripcion' )

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            cuentas_aspirantes = (Cuenta.objects.filter(rol=Rol.ASPIRANTE, activo=True).select_related('persona'))

            asignaciones = [PruebaUsuario(prueba=obj, persona=c.persona)for c in cuentas_aspirantes]
            PruebaUsuario.objects.bulk_create(asignaciones, ignore_conflicts=True)