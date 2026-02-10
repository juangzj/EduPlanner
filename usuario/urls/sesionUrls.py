from django.urls import path
from usuario.views import sesionViews

urlpatterns = [
    path("principal/", sesionViews.pagina_inicio_view, name="principal"),
    path("acceso/", sesionViews.inicio_de_sesion, name="acceso"),
    path("cerrar_sesion/", sesionViews.cerrar_sesion, name="cerrar_sesion"),
]
