from django.db import models
from EstructuraAcademica.models import PeriodoAcademico
from Usuarios.models import Persona
from Prueba.models import BancoPregunta, PreguntaOpcion

class Prueba(models.Model):
    fecha_realizacion=models.DateTimeField(auto_now_add=True)
    persona=models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='pruebas')
    periodo_academico=models.OneToOneField(PeriodoAcademico, on_delete=models.CASCADE, related_name='pruebas')

    def mostrarCarrerasAfines(self):
        pass

class ResultadoPorCarrera(models.Model):
    banco_pregunta=models.ForeignKey(BancoPregunta, on_delete=models.CASCADE, related_name='resultados_por_carrera', default=None)
    prueba=models.ForeignKey(Prueba, on_delete=models.CASCADE, related_name='resultados_por_carrera')

    def _str_(self):
        return f"Resultado de {self.carrera}"

    def calcularResultado(resultado):
        pass

class Resultado(models.Model):
    pregunta_opcion= models.ForeignKey(PreguntaOpcion, on_delete=models.CASCADE, related_name='resultados', default=None)
    resultado_por_carrera = models.ForeignKey(ResultadoPorCarrera, on_delete=models.CASCADE, related_name='resultados')

    def __str__(self):
       return f"Resultado {self.id}"

    def guardarTemporalmente(self):
        pass

