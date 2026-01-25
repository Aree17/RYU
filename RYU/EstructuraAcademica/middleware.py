from django.utils import timezone
from .models import PeriodoAcademico

class ActualizarPeriodoAcademicoMiddleware:
    # Actualiza automáticamente la vigencia de los periodos académicos según la fecha actual (lazy update)
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hoy = timezone.now().date()

        # 1. Desactivar todos los periodos vencidos o futuros
        PeriodoAcademico.objects.exclude(
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        ).filter(vigencia=True).update(vigencia=False)

        # 2. Activar solo el periodo vigente actual
        PeriodoAcademico.objects.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy,
            vigencia=False
        ).update(vigencia=True)

        return self.get_response(request)
