from django.db import models
from EstructuraAcademica.models import PeriodoAcademico, Carrera
# Create your models here.
class BancoPreguntas(models.Model):
    nombre = models.CharField(max_length=100)
    periodoVigente = models.ManyToManyField('EstructuraAcademica.PeriodoAcademico', related_name='bancos_preguntas',
    blank=True)
    carrera = models.ForeignKey('EstructuraAcademica.Carrera', on_delete=models.CASCADE, related_name='bancos_preguntas',null=True,
    blank=True)
    @property
    def vigente(self):
        return self.periodoVigente.filter(vigencia=True).exists()

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = "Banco de Preguntas"
        verbose_name_plural = "Banco de Preguntas"


class Opcion(models.Model):
    contenido = models.TextField()
    valor = models.IntegerField()
    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"

    def __str__(self):
        return self.contenido

class Pregunta(models.Model):
    enunciado = models.TextField()
    banco = models.ForeignKey('BancoPreguntas', on_delete=models.CASCADE, related_name='preguntas')
    opcion = models.ManyToManyField('Opcion', related_name='preguntas', blank=True)

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
    def __str__(self):
        return self.enunciado
