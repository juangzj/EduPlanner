import threading
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Importaciones del proyecto
from ..models.planeacionClaseGaide import PlaneacionClaseGaide
from ..forms.planeacionGaideForms import CreacionEstructuraPlaneacionClaseGaideForm
from ..services.ia_services import GaideIAService  

# Instanciamos el servicio a nivel de módulo o dentro de la vista
ia_service = GaideIAService()

@login_required 
def crear_planeacion_clase_gaide(request):
    """
    Paso 1: Captura metadatos y lanza la generación de la estructura inicial.
    """
    if request.method == 'POST':
        form = CreacionEstructuraPlaneacionClaseGaideForm(request.POST)
        if form.is_valid():
            planeacion = form.save(commit=False)
            planeacion.autor = request.user
            planeacion.save() 

            # Construimos el prompt inicial profesional
            prompt_inicial = (
                f"Genera una estructura de clase para el grado {planeacion.grado}. "
                f"Área: {planeacion.area}. Tema: {planeacion.tema}. "
                f"Objetivo: {planeacion.objetivo_aprendizaje}. Competencia: {planeacion.competencia}. "
                f"Información adicional: {planeacion.informacion_adicional or 'N/A'}"
            )

            # Ejecución asíncrona mediante hilos
            thread = threading.Thread(
                target=ia_service.procesar_flujo, 
                args=(planeacion.id, prompt_inicial, "estructura")
            )
            thread.start()

            messages.success(request, "¡Gaide está diseñando la estructura de tu clase! Por favor, espera.")
            return redirect('refinamientos_view', pk=planeacion.id) 
    else:
        form = CreacionEstructuraPlaneacionClaseGaideForm()

    return render(request, 'planeacion_de_clases_pags/formulario_creacion_estructura_clase_gaide.html', {'form': form})

@login_required
def refinamientos_view(request, pk):
    """
    Paso 2: Panel de interacción. Permite ver la estructura y solicitar cambios.
    """
    # Siempre filtramos por autor para que nadie vea planeaciones ajenas
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk, autor=request.user)
    
    # Si el docente envía una observación para refinar
    if request.method == 'POST' and not planeacion.planeacion_finalizada:
        observacion = request.POST.get('observacion')
        if observacion:
            # Limpiamos el contenido actual para que el frontend detecte "cargando"
            planeacion.contenido_generado = None
            planeacion.save()

            prompt_refinar = (
                f"Toma la estructura anterior y aplica estos refinamientos: {observacion}. "
                "Mantén el formato de estructura pedagógica."
            )

            threading.Thread(
                target=ia_service.procesar_flujo, 
                args=(planeacion.id, prompt_refinar, "refinar")
            ).start()
            
            return JsonResponse({'status': 'procesando'})

    return render(request, 'planeacion_de_clases_pags/refinamientos_pag.html', {'planeacion': planeacion})

@login_required
def generar_planeacion_final(request, pk):
    """
    Paso 3: Transforma la estructura aprobada en una planeación de clase completa.
    """
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        # Limpiamos para el estado de carga
        planeacion.contenido_generado = None
        planeacion.save()

        prompt_final = (
            f"Basado en esta estructura aprobada: {planeacion.contenido_generado}. "
            "Desarrolla ahora la planeación de clase completa, incluyendo actividades "
            "detalladas, tiempos, recursos y criterios de evaluación."
        )

        threading.Thread(
            target=ia_service.procesar_flujo, 
            args=(planeacion.id, prompt_final, "final")
        ).start()

        return JsonResponse({'status': 'generando_contenido_final'})

    return redirect('refinamientos_view', pk=pk)

@login_required
def verificar_estado_ia(request, pk):
    """
    Endpoint para que AJAX verifique si la IA terminó.
    """
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk, autor=request.user)
    contenido = planeacion.contenido_generado
    
    return JsonResponse({
        'finalizado': bool(contenido),
        'contenido': contenido if contenido else "",
        'error': "ERROR_IA" in (contenido or ""),
        'es_final': planeacion.planeacion_finalizada
    })
