from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from EstructuraAcademica.models import PeriodoAcademico
from Resultados.models import PruebaUsuario, Estado


@receiver(post_save, sender=PeriodoAcademico)
@transaction.atomic
def cambiar_estado_prueba(sender, instance, **kwargs):
    # Si el periodo sigue vigente, no hacemos nada
    if instance.vigencia:
        return

    # Cancelar SOLO PruebaUsuario en estado DISPONIBLE
    PruebaUsuario.objects.filter(
        prueba__periodo_academico=instance,
        estado__in=[Estado.DISPONIBLE, Estado.ENPROCESO]
    ).update(estado=Estado.CADUCADA)
