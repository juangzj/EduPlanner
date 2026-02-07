from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from ..forms.acceso_form import FormularioAcceso
from planeaciones_de_clases.models import PlaneacionClaseGaide
from django.db.models import Count


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
    # 1. ESTADÍSTICAS GENERALES
    # Total de planeaciones creadas en la plataforma
    total_planeaciones = PlaneacionClaseGaide.objects.count()
    
    # Total de docentes únicos que han interactuado (usando el campo autor)
    total_docentes = PlaneacionClaseGaide.objects.values('autor').distinct().count()
    
    # Total de recursos que los docentes han decidido publicar en el foro
    total_compartidos = PlaneacionClaseGaide.objects.filter(publicada=True).count()

    # 2. RECURSOS POPULARES
    # Traemos las 3 planeaciones publicadas que tengan más likes.
    # Usamos 'annotate' para contar los likes de cada planeación en una sola consulta.
    recursos_populares = PlaneacionClaseGaide.objects.filter(publicada=True)\
        .annotate(num_likes=Count('likes'))\
        .order_by('-num_likes', '-fecha_creacion')[:3]

    context = {
        'total_planeaciones': total_planeaciones,
        'total_docentes': total_docentes,
        'total_compartidos': total_compartidos,
        'recursos_populares': recursos_populares,
    }
    
    return render(request, "inicio_pag.html", context)