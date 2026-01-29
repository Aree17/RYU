from django.shortcuts import render, get_object_or_404
from EstructuraAcademica.models import Carrera

def carrera_detalle_view(request, carrera_id):
    carrera = get_object_or_404(Carrera, id=carrera_id)
    malla_vigente = (
        carrera.mallas
        .filter(vigente=True)
        .order_by('-id')
        .first()
    )
    return render(request, "Resultados/carrera_detalle.html", {"carrera": carrera, "malla_vigente": malla_vigente,})