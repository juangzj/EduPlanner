"""
En este archivo esta la logica de noegocio
"""

from ..forms import LoginForm, RegistroForm
from ..models import UsuarioPersonalizado


def registar_usuario_servicio(data):
    usuario = UsuarioPersonalizado()

    usuario.save
    return usuario
