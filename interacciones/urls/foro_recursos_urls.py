from django.urls import path
from ..views import foro_recursos_views
from ..views import comentario_views
from ..views import like_views


urlpatterns = [

    path("foro-recursos/", foro_recursos_views.foro_recursos, name="foro_recursos"),
    path('foro/planeacion/<int:pk>/', foro_recursos_views.foro_planeacion_detalle, name='foro_planeacion_detalle'),
    path('foro/planeacion/<int:pk>/comentar/', comentario_views.agregar_comentario, name='agregar_comentario'),
    path('foro/planeacion/<int:pk>/like/', like_views.toggle_like, name='toggle_like'),
]




