from django.contrib import admin
from .models import Facultad, Carrera, MallaCurricular, PeriodoAcademico


@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'siglas')
    search_fields = ('nombre', 'siglas')
    ordering = ('nombre',)


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'facultad', 'duracion_anios')
    list_filter = ('facultad',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


@admin.register(MallaCurricular)
class MallaCurricularAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'carrera', 'vigente')
    list_filter = ('vigente', 'carrera')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(PeriodoAcademico)
class PeriodoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'vigencia')
    list_filter = ('vigencia',)
    search_fields = ('nombre',)
    date_hierarchy = 'fecha_inicio'
    ordering = ('-fecha_inicio',)
