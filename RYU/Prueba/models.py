from django.db import models
from EstructuraAcademica.models import PeriodoAcademico, Carrera
# Create your models here.
class BancoPregunta(models.Model):
    nombre = models.CharField(max_length=100)
    vigente = models.BooleanField(default=False)
    periodoVigente = models.ManyToManyField('EstructuraAcademica.PeriodoAcademico', related_name='bancos_pregunta',
    blank=True)
    carrera = models.ForeignKey('EstructuraAcademica.Carrera', on_delete=models.CASCADE, related_name='bancos_pregunta',null=True,
    blank=True)

    class Meta:
        verbose_name = "Banco de preguntas"
        verbose_name_plural = "Banco de preguntas"

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    enunciado = models.TextField()
    banco = models.ForeignKey('BancoPregunta', on_delete=models.CASCADE, related_name='pregunta')

    class Meta:
        verbose_name = "Pregunta"
        verbose_name_plural = "Preguntas"
    def __str__(self):
        return self.enunciado

class Opcion(models.Model):
    contenido = models.TextField()
    valor = models.IntegerField()

    class Meta:
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"

    def __str__(self):
        return self.contenido

class PreguntaOpcion(models.Model):
    pregunta = models.ForeignKey('Pregunta', on_delete=models.CASCADE, related_name='opcion')
    opcion = models.ForeignKey('Opcion', on_delete=models.CASCADE, related_name='pregunta')

    class Meta:
        verbose_name = "Opción de pregunta"
        verbose_name_plural = "Opciones de pregunta"