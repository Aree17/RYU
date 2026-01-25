from django.urls import path
from . import views

urlpatterns = [
    path("carreras/<int:carrera_id>/", views.carrera_detalle_view, name="carrera_detail"),
]
