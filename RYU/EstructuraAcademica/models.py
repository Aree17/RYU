from django.db import models

class Facultad(models.Model):
    nombre = models.CharField(max_length=100)
    siglas = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Facultad"
        verbose_name_plural = "Facultades"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.siglas})"

class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_anios = models.IntegerField()
    perfil_ingreso = models.TextField()
    perfil_egreso = models.TextField()

    facultad = models.ForeignKey(
        Facultad,
        on_delete=models.CASCADE,
        related_name="carreras"
    )

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class MallaCurricular(models.Model):
    nombre = models.CharField(max_length=100)
    ruta_pdf = models.CharField(max_length=255)
    vigente = models.BooleanField(default=True)

    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.CASCADE,
        related_name="mallas"
    )

    class Meta:
        verbose_name = "Malla Curricular"
        verbose_name_plural = "Mallas Curriculares"

    def __str__(self):
        return f"{self.nombre} - {self.carrera.nombre}"

class PeriodoAcademico(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    vigencia = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Periodo Académico"
        verbose_name_plural = "Periodos Académicos"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return self.nombre
