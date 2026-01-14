from django.db import models
# Create your models here.

class BancoPregunta(models.Model):
    nombre = models.CharField(max_length=50)
    vigente = models.BooleanField()

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    enunciado = models.TextField(max_length=500)
    banco_pregunta = models.ForeignKey(BancoPregunta, on_delete=models.CASCADE, related_name='banco_pregunta')


class Opcion (models.Model):
    contenido = models.CharField(max_length=10)
    valor = models.IntegerField()

    def __str__(self):
        return self.contenido

class PreguntaOpcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='pregunta')
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE, related_name='opcion')