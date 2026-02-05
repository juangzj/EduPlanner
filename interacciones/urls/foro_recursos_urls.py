from django.urls import path
from ..views import foro_recursos_views

urlpatterns = [

    path("foro-recursos/", foro_recursos_views.foro_recursos, name="foro_recursos"),
]