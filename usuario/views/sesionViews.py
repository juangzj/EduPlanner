from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from ..forms.acceso_form import FormularioAcceso


def inicio_de_sesion(request):
    form = FormularioAcceso()

    if request.method == "POST":
        form = FormularioAcceso(request.POST)
        if form.is_valid():
            gmail = form.cleaned_data["gmail"]
            contrasena = form.cleaned_data["contrasena"]
            usuario = authenticate(request, username=gmail, password=contrasena)

            if usuario is not None:
                login(request, usuario)
                messages.success(
                    request, f"Bienvenido {usuario.apodo or usuario.gmail}"
                )
                return redirect("principal")
            else:
                messages.error(request, "Correo o contraseña incorrectos")

    return render(request, "inicio_de_sesion_pag.html", {"form": form})


# Panel principal
@login_required
def pagina_inicio_view(request):
    return render(request, "inicio_pag.html")
