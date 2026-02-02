import json
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from EstructuraAcademica.models import PeriodoAcademico
from Prueba.models import Pregunta, Opcion
from Resultados.models import PruebaUsuario, ResultadoPorCarrera, Estado
from Resultados.services import registrar_respuesta, finalizar_prueba, top_carreras_global, \
    tasa_finalizacion_por_prueba, promedio_por_carrera, top_carreras_por_periodo, \
    tasa_finalizacion_por_periodo, promedio_carrera_por_periodo
from Usuarios.models import Cuenta


@login_required
def resolver_prueba_view(request, prueba_usuario_id):
    prueba_usuario = get_object_or_404(PruebaUsuario, id=prueba_usuario_id, persona=request.user.cuenta.persona)
    if prueba_usuario.estado == Estado.CADUCADA:
        messages.error(request, "Esta prueba fue cancelada y no se puede resolver.")
        return redirect("home")

    if prueba_usuario.estado == Estado.FINALIZADA:
        messages.info(request, "Esta prueba ya fue realizada.")
        return redirect("visualizar_resultados", prueba_usuario.id)

    if prueba_usuario.estado == Estado.DISPONIBLE:
        prueba_usuario.estado = Estado.ENPROCESO
        prueba_usuario.save(update_fields=["estado"])

    periodo = prueba_usuario.prueba.periodo_academico
    preguntas = (Pregunta.objects.filter(banco__periodoVigente=periodo).select_related("banco"))
    opciones = Opcion.objects.all().order_by("id")

    return render(request, "Prueba/prueba.html", {
        "prueba_usuario": prueba_usuario, "preguntas": preguntas, "opciones": opciones})

@login_required(login_url="login")
@require_POST
def guardar_respuesta_view(request, prueba_usuario_id):
    prueba_usuario = get_object_or_404(PruebaUsuario,id=prueba_usuario_id,persona=request.user.cuenta.persona)

    if prueba_usuario.estado == Estado.CADUCADA:
        messages.error(request, "Esta prueba fue cancelada y no se puede resolver.")
        return redirect("home")

    if prueba_usuario.estado == Estado.FINALIZADA:
        messages.info(request, "Esta prueba ya fue finalizada.")
        return redirect("visualizar_resultados", prueba_usuario_id=prueba_usuario_id)

    try:
        for key, value in request.POST.items():
            if key.startswith("pregunta_"):
                pregunta_id = int(key.replace("pregunta_", ""))
                opcion_id = int(value)

                registrar_respuesta(prueba_usuario_id=prueba_usuario_id, pregunta_id=pregunta_id, opcion_id=opcion_id)

        finalizar_prueba(prueba_usuario_id)
        return redirect("visualizar_resultados", prueba_usuario_id=prueba_usuario_id)

    except (ValidationError, ValueError) as e:
        messages.error(request, str(e))
        return redirect("resolver_prueba", prueba_usuario_id=prueba_usuario_id)

@login_required(login_url="login")
@require_POST
def abandonar_prueba_view(request, prueba_usuario_id):
    pu = get_object_or_404(
        PruebaUsuario,
        id=prueba_usuario_id,
        persona=request.user.cuenta.persona
    )

    if pu.estado == Estado.ENPROCESO:
        pu.estado = Estado.DISPONIBLE
        pu.save(update_fields=["estado"])

    return JsonResponse({"ok": True})


@login_required(login_url="login")
def visualizar_resultados_view(request, prueba_usuario_id):
    cuenta = get_object_or_404(Cuenta, user=request.user)
    prueba_usuario = get_object_or_404(PruebaUsuario, id=prueba_usuario_id, persona=cuenta.persona if cuenta else None)
    resultados = (ResultadoPorCarrera.objects.filter(prueba_usuario=prueba_usuario).select_related("banco_pregunta__carrera")
        .order_by("-resultado_total"))

    labels = [r.banco_pregunta.nombre for r in resultados]
    values = [int(r.resultado_total or 0) for r in resultados]

    top3 = [
        {
            "carrera_id": r.banco_pregunta.carrera.id if r.banco_pregunta.carrera else None,
            "carrera": r.banco_pregunta.carrera.nombre if r.banco_pregunta.carrera else "Sin carrera",
            "banco": r.banco_pregunta.carrera.nombre,
            "puntaje": int(r.resultado_total or 0),
        }
        for r in resultados[:3]
    ]

    context = {
        "prueba_usuario": prueba_usuario,
        "labels_json": json.dumps(labels),
        "values_json": json.dumps(values),
        "top3": top3,
    }
    return render(request, "Resultados/resultados.html", context)


# VISTAS PARA ADMIN
@staff_member_required(login_url="login")
def dashboard_resultados(request):
    scope = request.GET.get("scope", "global")
    periodo_id = request.GET.get("periodo_id")

    periodos = PeriodoAcademico.objects.all().order_by("-id")

    periodo_ok = bool(periodo_id) and str(periodo_id).isdigit()

    if scope == "periodo" and periodo_ok:
        pid = int(periodo_id)

        top_carreras = list(top_carreras_por_periodo(pid, limit=10))
        tasa_por_prueba = tasa_finalizacion_por_periodo(pid)
        promedios = list(promedio_carrera_por_periodo(pid))

    elif scope == "periodo" and not periodo_ok:
        top_carreras = []
        tasa_por_prueba = []
        promedios = []

    else:
        scope = "global"
        top_carreras = list(top_carreras_global(limit=10))
        tasa_por_prueba = tasa_finalizacion_por_prueba()
        promedios = list(promedio_por_carrera())

    return render(request, "admin/dashboard_resultados.html", {
        "periodos": periodos,
        "scope": scope,
        "periodo_id": int(periodo_id) if periodo_ok else None,
        "top_carreras": top_carreras,
        "tasa_por_prueba": tasa_por_prueba,
        "promedios": promedios,
    })
