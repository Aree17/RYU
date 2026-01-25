from django.db import transaction
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from Prueba.models import Pregunta, Opcion
from Usuarios.models import Cuenta, Rol
from .models import PruebaUsuario, BancoPreguntas, ResultadoPorCarrera, Respuesta, Estado


def obtener_bancos_del_periodo(periodo):
    return (BancoPreguntas.objects.filter(periodoVigente=periodo, periodoVigente__vigencia=True).distinct())

@transaction.atomic
def crear_prueba_usuario_con_resultados(prueba, persona):
    pu, created = PruebaUsuario.objects.get_or_create(
        prueba=prueba, persona=persona, defaults={"estado": Estado.DISPONIBLE, "fecha_realizacion": None})

    if not created:
        return pu

    bancos = obtener_bancos_del_periodo(prueba.periodo_academico)

    if not bancos.exists():
        raise ValidationError(
            "No existen bancos de preguntas asociados al periodo académico vigente."
        )

    resultados = [
        ResultadoPorCarrera(prueba_usuario=pu, banco_pregunta=banco, resultado_total=0)
        for banco in bancos
    ]

    ResultadoPorCarrera.objects.bulk_create(resultados, ignore_conflicts=True)

    return pu

@transaction.atomic
def asignar_prueba_a_aspirantes(prueba):
    cuentas = ( Cuenta.objects .filter(rol=Rol.ASPIRANTE, activo=True) .select_related("persona"))

    for cuenta in cuentas:
        crear_prueba_usuario_con_resultados(prueba=prueba, persona=cuenta.persona)

@transaction.atomic
def registrar_respuesta(prueba_usuario_id: int, pregunta_id: int, opcion_id: int) -> Respuesta:
    prueba_usuario = PruebaUsuario.objects.select_for_update().get(id=prueba_usuario_id)
    pregunta = Pregunta.objects.select_related("banco").get(id=pregunta_id)
    opcion = Opcion.objects.get(id=opcion_id)

    try:
        rpc = ResultadoPorCarrera.objects.select_for_update().get(
            prueba_usuario=prueba_usuario,
            banco_pregunta=pregunta.banco
        )
    except ResultadoPorCarrera.DoesNotExist:
        raise ValidationError(
            "No existe ResultadoPorCarrera para este banco en esta Prueba."
        )

    respuesta, _ = Respuesta.objects.update_or_create(
        resultado_por_carrera=rpc,
        pregunta=pregunta,
        defaults={"opcion": opcion}
    )
    return respuesta

@transaction.atomic
def finalizar_prueba(prueba_usuario_id: int) -> None:
    prueba_usuario = PruebaUsuario.objects.select_for_update().get(id=prueba_usuario_id)

    if prueba_usuario.estado == Estado.FINALIZADA:
        return

    total_preguntas = Pregunta.objects.filter(banco__in=ResultadoPorCarrera.objects.filter(
        prueba_usuario=prueba_usuario).values("banco_pregunta")).count()

    respondidas = Respuesta.objects.filter(resultado_por_carrera__prueba_usuario=prueba_usuario).values("pregunta_id").distinct().count()

    if respondidas < total_preguntas:
        raise ValidationError(
            f"Debes responder todas las preguntas antes de finalizar " f"({respondidas}/{total_preguntas}).")

    respuestas = (
        Respuesta.objects.filter(resultado_por_carrera__prueba_usuario=prueba_usuario).select_related("opcion"))

    acumulado = {}
    for r in respuestas:
        rpc_id = r.resultado_por_carrera_id
        acumulado[rpc_id] = acumulado.get(rpc_id, 0) + r.opcion.valor

    resultados = ResultadoPorCarrera.objects.filter(prueba_usuario=prueba_usuario)
    for rpc in resultados:
        rpc.resultado_total = acumulado.get(rpc.id, 0)
        rpc.save(update_fields=["resultado_total"])

    prueba_usuario.estado = Estado.FINALIZADA
    prueba_usuario.fecha_realizacion = timezone.now()
    prueba_usuario.save(update_fields=["estado", "fecha_realizacion"])

def top_carreras_global(limit=10):
    return (
        ResultadoPorCarrera.objects
        .filter(prueba_usuario__estado=Estado.FINALIZADA)
        .values("banco_pregunta__carrera__id", "banco_pregunta__carrera__nombre")
        .annotate(total=Sum("resultado_total"))
        .order_by("-total")[:limit]
    )

def top_carreras_por_periodo(periodo_id, limit=10):
    return (
        ResultadoPorCarrera.objects
        .filter(
            prueba_usuario__estado=Estado.FINALIZADA,
            prueba_usuario__prueba__periodo_academico_id=periodo_id
        )
        .values("banco_pregunta__carrera__id", "banco_pregunta__carrera__nombre")
        .annotate(total=Sum("resultado_total"))
        .order_by("-total")[:limit]
    )

def tasa_finalizacion_por_prueba():  # GLOBAL
    rows = (
        PruebaUsuario.objects
        .values("prueba__id", "prueba__titulo")
        .annotate(asignadas=Count("id"), finalizadas=Count("id", filter=Q(estado=Estado.FINALIZADA)),)
        .order_by("-finalizadas")
    )

    result = []
    for r in rows:
        asignadas = r["asignadas"] or 0
        finalizadas = r["finalizadas"] or 0
        r["tasa"] = round((finalizadas / asignadas) * 100, 2) if asignadas else 0
        result.append(r)
    return result

def tasa_finalizacion_por_periodo(periodo_id):
    rows = (
        PruebaUsuario.objects
        .filter(prueba__periodo_academico_id=periodo_id)
        .values("prueba__id", "prueba__titulo")
        .annotate(asignadas=Count("id"),finalizadas=Count("id", filter=Q(estado=Estado.FINALIZADA)),)
        .order_by("-finalizadas")
    )

    result = []
    for r in rows:
        asignadas = r["asignadas"] or 0
        finalizadas = r["finalizadas"] or 0
        r["tasa"] = round((finalizadas / asignadas) * 100, 2) if asignadas else 0
        result.append(r)
    return result

def promedio_por_carrera():
    return (
        ResultadoPorCarrera.objects
        .filter(prueba_usuario__estado=Estado.FINALIZADA)
        .values("banco_pregunta__carrera__id", "banco_pregunta__carrera__nombre")
        .annotate(promedio=Avg("resultado_total"))
        .order_by("-promedio")
    )

def promedio_carrera_por_periodo(periodo_id):
    return (
        ResultadoPorCarrera.objects
        .filter(prueba_usuario__estado=Estado.FINALIZADA,prueba_usuario__prueba__periodo_academico_id=periodo_id)
        .values("banco_pregunta__carrera__id", "banco_pregunta__carrera__nombre")
        .annotate(promedio=Avg("resultado_total"))
        .order_by("-promedio")
    )