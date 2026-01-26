from django.urls import path
from ..views import planeacionClaseGaideViews

urlpatterns = [
    path("crear-estructura-planeacion-clase-gaide/", planeacionClaseGaideViews.crear_planeacion_clase_gaide, name="crear_planeacion_clase_gaide"),
    path("refinamientos/<int:pk>/", planeacionClaseGaideViews.refinamientos_view, name="refinamientos_view" ),
    path("verificar-estado-ia/<int:pk>/", planeacionClaseGaideViews.verificar_estado_ia, name="verificar_estado_ia"),

]