
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.comentarioPlaneacion import ComentarioPlaneacion
from planeaciones_de_clases.models import PlaneacionClaseGaide

@login_required
def agregar_comentario(request, pk):
    if request.method == "POST":
        planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk)
        contenido = request.POST.get('contenido')
        
        if contenido:
            ComentarioPlaneacion.objects.create(
                planeacion=planeacion,
                autor=request.user,
                contenido=contenido
            )
            messages.success(request, "Tu comentario ha sido publicado.")
        else:
            messages.error(request, "El comentario no puede estar vacío.")
            
    return redirect('interacciones_pags/foro_planeacion_detalle/', pk=pk)