from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from planeaciones_de_clases.models import PlaneacionClaseGaide

@login_required
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


@login_required
def foro_planeacion_detalle(request, pk):
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk)
    
    # Obtener comentarios activos
    comentarios = planeacion.comentarios.filter(activo=True).order_by('-fecha_creacion')
    
    # Verificar si el usuario actual ya dio like
    user_has_liked = planeacion.likes.filter(usuario=request.user).exists()
    
    # Conteo de likes
    total_likes = planeacion.likes.count()

    return render(request, 'interacciones_pags/foro_planeacion_detalle.html', {
        'planeacion': planeacion,
        'comentarios': comentarios,
        'user_has_liked': user_has_liked,
        'total_likes': total_likes,
        'es_dueno': planeacion.autor == request.user 
    })