import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from ..models.planeacionClaseGaide import PlaneacionClaseGaide
from ..forms.planeacionGaideForms import CreacionEstructuraPlaneacionClaseGaideForm
from ..services.ia_services import GaideIAService


ia_service = GaideIAService()


@login_required
def crear_planeacion_clase_gaide(request):
    """
    Paso 1: Captura metadatos y genera la estructura inicial
    """
    if request.method == 'POST':
        form = CreacionEstructuraPlaneacionClaseGaideForm(request.POST)
        if form.is_valid():
            planeacion = form.save(commit=False)
            planeacion.autor = request.user
            planeacion.save()

            threading.Thread(
                target=ia_service.procesar_flujo,
                args=(planeacion.id, "", "estructura")
            ).start()

            messages.success(
                request,
                "Gaide está generando la estructura de tu clase. Espera un momento."
            )

            return redirect('refinamientos_view', pk=planeacion.id)
    else:
        form = CreacionEstructuraPlaneacionClaseGaideForm()

    return render(
        request,
        'planeacion_de_clases_pags/formulario_creacion_estructura_clase_gaide.html',
        {'form': form}
    )

@login_required
def refinamientos_view(request, pk):
    """
    Paso 2: Ver estructura y solicitar refinamientos
    """
    planeacion = get_object_or_404(
        PlaneacionClaseGaide,
        pk=pk,
        autor=request.user
    )

    if request.method == 'POST' and not planeacion.planeacion_finalizada:
        observacion = request.POST.get('observacion')

        if observacion:
            threading.Thread(
                target=ia_service.procesar_flujo,
                args=(planeacion.id, observacion, "refinar")
            ).start()

            return JsonResponse({'status': 'procesando'})

    return render(
        request,
        'planeacion_de_clases_pags/refinamientos_pag.html',
        {'planeacion': planeacion}
    )


@login_required
def generar_planeacion_final(request, pk):
    """
    Paso 3: Genera la planeacion completa
    """
    planeacion = get_object_or_404(
        PlaneacionClaseGaide,
        pk=pk,
        autor=request.user
    )

    if request.method == 'POST':
        threading.Thread(
            target=ia_service.procesar_flujo,
            args=(planeacion.id, "", "final")
        ).start()

        return JsonResponse({'status': 'generando_final'})

    return redirect('refinamientos_view', pk=pk)



@login_required
def verificar_estado_ia(request, pk):
    """
    Endpoint AJAX para verificar si la IA terminó
    """
    planeacion = get_object_or_404(
        PlaneacionClaseGaide,
        pk=pk,
        autor=request.user
    )

    contenido = planeacion.contenido_generado or ""

    return JsonResponse({
        'finalizado': bool(contenido),
        'contenido': contenido,
        'error': contenido.startswith("ERROR_IA"),
        'es_final': planeacion.planeacion_finalizada
    })

@login_required
def cambiar_estado_publicacion(request, pk):
    """
    Maneja:
    - Finalizar sin publicar
    - Finalizar y publicar
    - Publicar (si ya estaba finalizada)
    - Quitar publicacion (si ya estaba publicada)
    """
    if request.method != 'POST':
        return redirect('refinamientos_view', pk=pk)

    planeacion = get_object_or_404(
        PlaneacionClaseGaide,
        pk=pk,
        autor=request.user
    )

    accion = request.POST.get('accion')

    # ===============================
    # CASO 1: NO ESTA FINALIZADA
    # ===============================
    if not planeacion.planeacion_finalizada:
        planeacion.planeacion_finalizada = True

        if accion == "finalizar_publicar":
            planeacion.publicada = True
            messages.success(
                request,
                "La planeacion fue finalizada y publicada correctamente."
            )
        else:
            planeacion.publicada = False
            messages.success(
                request,
                "La planeacion fue finalizada correctamente (no publicada)."
            )

    # ===============================
    # CASO 2: YA ESTA FINALIZADA
    # ===============================
    else:
        if accion == "publicar":
            planeacion.publicada = True
            messages.success(
                request,
                "La planeacion fue publicada correctamente."
            )

        elif accion == "quitar_publicacion":
            planeacion.publicada = False
            messages.success(
                request,
                "La planeacion fue retirada de publicacion."
            )

    planeacion.save()
    return redirect('refinamientos_view', pk=pk)
