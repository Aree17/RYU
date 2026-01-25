from django.db import models
from EstructuraAcademica.models import PeriodoAcademico
from Usuarios.models import Persona
from Prueba.models import BancoPreguntas, Pregunta, Opcion

class Estado(models.TextChoices):
    DISPONIBLE = "DISPONIBLE"
    ENPROCESO = "ENPROCESO"
    FINALIZADA = "FINALIZADA"
    CADUCADA = "CADUCADA"

class Prueba(models.Model):
    titulo=models.TextField(default="")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion = models.TextField(default="")
    periodo_academico = models.OneToOneField(PeriodoAcademico, on_delete=models.CASCADE, related_name='pruebas')
    def __str__(self):
        return f"{self.titulo}"

class PruebaUsuario(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='pruebas_usuario')
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE, related_name='usuarios')
    fecha_realizacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE
    )

    def __str__(self):
        return f"Prueba de {self.persona} - {self.prueba}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['persona', 'prueba'],name='unique_prueba_por_persona')]

    def save(self, *args, **kwargs):
        periodo = self.prueba.periodo_academico
        if hasattr(periodo, "vigente") and not periodo.vigente:
            if self.estado in [Estado.DISPONIBLE, Estado.ENPROCESO]:
                self.estado = Estado.CADUCADA
        super().save(*args, **kwargs)


class ResultadoPorCarrera(models.Model):
    banco_pregunta = models.ForeignKey(BancoPreguntas, on_delete=models.CASCADE, related_name='resultados_por_carrera', default=None)
    prueba_usuario = models.ForeignKey(PruebaUsuario, on_delete=models.CASCADE, related_name='resultados_por_carrera')
    resultado_total= models.IntegerField(default=0)
    def __str__(self):
        return f"{self.prueba_usuario.persona} - Carrera: {self.banco_pregunta.carrera}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["prueba_usuario", "banco_pregunta"],
                name="unique_resultado_por_banco_prueba_usuario"
            )
        ]



class Respuesta(models.Model):
    resultado_por_carrera = models.ForeignKey(ResultadoPorCarrera, on_delete=models.CASCADE, related_name='respuestas_usuario', null=True, blank=True)
    pregunta = models.ForeignKey(Pregunta,on_delete=models.CASCADE,related_name='respuestas')
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE, related_name='respuestas')

    def __str__(self):
        return f"Respuesta a {self.pregunta} - Opción: {self.opcion}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['resultado_por_carrera', 'pregunta'],name='unique_respuesta_por_pregunta')]
