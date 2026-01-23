from django.urls import path
from ..views import planeacionClaseGaideViews

urlpatterns = [
    path("crear-estructura-planeacion-clase-gaide/", planeacionClaseGaideViews.crear_planeacion_clase_gaide, name="crear_planeacion_clase_gaide")

]