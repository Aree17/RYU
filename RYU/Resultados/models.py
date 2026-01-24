from django.db import models
from EstructuraAcademica.models import PeriodoAcademico
from Usuarios.models import Persona
from Prueba.models import BancoPreguntas, Pregunta

class Estado(models.TextChoices):
    DISPONIBLE = "DISPONIBLE"
    ENPROCESO = "ENPROCESO"
    FINALIZADA = "FINALIZADA"

class Prueba(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField()


class PruebaUsuario(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='pruebas_usuario')
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, related_name='usuarios')
    fecha_realizacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['persona', 'prueba'],
                name='unique_prueba_por_persona'
            )
        ]


class ResultadoPorCarrera(models.Model):
    banco_pregunta=models.ForeignKey(BancoPreguntas, on_delete=models.CASCADE, related_name='resultados_por_carrera', default=None)
    prueba=models.ForeignKey(Prueba, on_delete=models.CASCADE, related_name='resultados_por_carrera')


class Respuesta(models.Model):
    pregunta_opcion= models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas', default=None)
    resultado_por_carrera = models.ForeignKey(ResultadoPorCarrera, on_delete=models.CASCADE, related_name='respuestas_usuario')

