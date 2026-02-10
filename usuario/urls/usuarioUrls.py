from django.urls import path
from usuario.views import usuarioViews 

urlpatterns = [
    path(
        "usuarios/registro/",
        usuarioViews.registrar_usuario_view,
        name="registrar_usuario",
    ),
    path('perfil/editar/',usuarioViews.editar_perfil, name='editar_perfil'),
]
