from django.shortcuts import render
from django.db.models import Count
from planeaciones_de_clases.models import PlaneacionClaseGaide

def foro_recursos(request):
    # Filtramos solo las que están marcadas como publicadas
    # Usamos annotate para traer el conteo de likes y comentarios
    planeaciones = PlaneacionClaseGaide.objects.filter(publicada=True).annotate(
        total_likes=Count('likes', distinct=True),
        total_comentarios=Count('comentarios', distinct=True)
    ).order_by('-fecha_creacion')

    context = {
        'planeaciones': planeaciones,
    }
    return render(request, 'interacciones_pags/foro_recursos.html', context)