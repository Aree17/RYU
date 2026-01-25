import logging
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from EstructuraAcademica.models import PeriodoAcademico
from Resultados.models import PruebaUsuario, ResultadoPorCarrera, Prueba, Estado  # ajusta según tu app
from Prueba.models import BancoPreguntas  # ajusta según tu app/ruta

logger = logging.getLogger(__name__)

@receiver(post_save, sender=PruebaUsuario)
def crear_resultados_por_carrera(sender, instance: PruebaUsuario, created: bool, **kwargs):
    if not created:
        return

    def _after_commit():
        try:
            periodo = instance.prueba.periodo_academico
            bancos = BancoPreguntas.objects.filter(periodoVigente=periodo).distinct()

            for banco in bancos:
                ResultadoPorCarrera.objects.get_or_create(
                    prueba=instance,
                    banco_pregunta=banco,
                    resultado_total=0,
                    defaults={}
                )

        except Exception as e:
            logger.exception(
                "Error creando ResultadosPorCarrera para PruebaUsuario id=%s: %s",
                instance.id, str(e)
            )

    transaction.on_commit(_after_commit)
