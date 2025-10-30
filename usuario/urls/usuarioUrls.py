from django.urls import path
from usuario.views import usuarioViews

urlpatterns = [
    path(
        "usuarios/registro/",
        usuarioViews.registrar_usuario_view,
        name="registrar_usuario",
    ),
]
