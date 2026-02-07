from django.urls import path
from ..views import planeacionClaseGaideViews

urlpatterns = [
    # Paso 1: Formulario inicial
    path(
        "crear-estructura-planeacion-clase-gaide/", 
        planeacionClaseGaideViews.crear_planeacion_clase_gaide, 
        name="crear_planeacion_clase_gaide"
    ),
    
    # Paso 2: Panel de interacción y refinamiento (donde el usuario chatea con la IA)
    path(
        "refinamientos/<int:pk>/", 
        planeacionClaseGaideViews.refinamientos_view, 
        name="refinamientos_view" 
    ),
    
    # Paso 3: Acción para convertir la estructura en contenido detallado (ESTA TE FALTABA)
    path(
        "generar-planeacion-final/<int:pk>/", 
        planeacionClaseGaideViews.generar_planeacion_final, 
        name="generar_planeacion_final"
    ),

    # Soporte: Endpoint para que el JavaScript (AJAX) pregunte si la IA ya terminó
    path(
        "verificar-estado-ia/<int:pk>/", 
        planeacionClaseGaideViews.verificar_estado_ia, 
        name="verificar_estado_ia"
    ),
  
]   