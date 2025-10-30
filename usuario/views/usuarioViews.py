from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ..forms import usuario_form


def registrar_usuario_view(request):
    if request.method == "POST":
        form = usuario_form.RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(
                request, "✅ El usuario se creó correctamente. Bienvenido/a."
            )
            return redirect("principal")
        else:
            messages.error(
                request,
                "❌ El formulario contiene errores. Revisa los campos marcados.",
            )
    else:
        form = usuario_form.RegistroForm()

    return render(request, "registrar_usuario_pag.html", {"form": form})
