from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path(
        "Prueba/<int:prueba_usuario_id>/",views.resolver_prueba_view,name="resolver_prueba"),
    path(
        "Prueba/<int:prueba_usuario_id>/responder/",views.guardar_respuesta_view,name="guardar_respuesta"),
    path(
        "Resultados/<int:prueba_usuario_id>/", views.visualizar_resultados_view, name="visualizar_resultados"),
    path("reportes/dashboard/", views.dashboard_resultados, name="dashboard_resultados"),
]

