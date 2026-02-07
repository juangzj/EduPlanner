
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.likePlaneacion import LikePlaneacion
from planeaciones_de_clases.models import PlaneacionClaseGaide


@login_required
def toggle_like(request, pk):
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk)
    like_qs = LikePlaneacion.objects.filter(planeacion=planeacion, usuario=request.user)

    if like_qs.exists():
        like_qs.delete()
    else:
        LikePlaneacion.objects.create(planeacion=planeacion, usuario=request.user)
        
    return redirect('interacciones_pags/foro_planeacion_detalle/', pk=pk)