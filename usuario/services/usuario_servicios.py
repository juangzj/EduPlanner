"""
En este archivo esta la logica de negocio
"""

from ..forms import LoginForm, RegistroForm
from ..models import UsuarioDocente


def registar_usuario_servicio(data):
    usuario = UsuarioDocente()

    usuario.save
    return usuario
