import threading
import os  # Para leer variables de entorno
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from openai import OpenAI
from ..forms.planeacionGaideForms import CreacionEstructuraPlaneacionClaseGaideForm
from ..models.planeacionClaseGaide import PlaneacionClaseGaide

def procesar_planeacion_con_ia(planeacion_id, datos_dict):
    """
    Lógica de IA en segundo plano utilizando variables de entorno.
    """
    from ..models.planeacionClaseGaide import PlaneacionClaseGaide
    
    # Extraemos la API Key del entorno (configurada previamente en tu .env)
    api_key_env = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key_env)

    try:
        prompt_estricto = f"""
        Actúa como docente experto en educación media y diseñador instruccional.
        Tu tarea es crear únicamente la estructura de una clase, sin desarrollar contenidos.
        Reglas estrictas:
        1. No desarrolles contenidos ni expliques conceptos.
        2. No escribas ejemplos extensos.
        3. Solo entrega la estructura organizada y bien explicada.

        Contexto:
        Grado: {datos_dict['grado']} | Área: {datos_dict['area']} | Tema: {datos_dict['tema']}
        Competencia: {datos_dict['competencia']}
        Objetivos: {datos_dict['objetivo']}
        Duración: {datos_dict['duracion']} | Nivel: {datos_dict['nivel']}
        Adicional: {datos_dict['adicional']}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un diseñador instruccional que solo entrega estructuras de clase."},
                {"role": "user", "content": prompt_estricto}
            ],
            temperature=0.3
        )

        resultado = response.choices[0].message.content
        PlaneacionClaseGaide.objects.filter(id=planeacion_id).update(contenido_generado=resultado)

    except Exception as e:
        PlaneacionClaseGaide.objects.filter(id=planeacion_id).update(
            contenido_generado=f"ERROR_IA: {str(e)}"
        )
    finally:
        connection.close()

@login_required 
def crear_planeacion_clase_gaide(request):
    if request.method == 'POST':
        form = CreacionEstructuraPlaneacionClaseGaideForm(request.POST)
        if form.is_valid():
            planeacion = form.save(commit=False)
            planeacion.autor = request.user
            planeacion.save() 

            datos_ia = {
                'grado': form.cleaned_data.get('grado'),
                'area': form.cleaned_data.get('area'),
                'tema': form.cleaned_data.get('tema'),
                'objetivo': form.cleaned_data.get('objetivo_aprendizaje'),
                'competencia': form.cleaned_data.get('competencia'),
                'duracion': form.cleaned_data.get('duracion_clase', 'No especificada'),
                'nivel': form.cleaned_data.get('nivel_grupo'),
                'adicional': form.cleaned_data.get('informacion_adicional'),
            }

            thread = threading.Thread(target=procesar_planeacion_con_ia, args=(planeacion.id, datos_ia))
            thread.start()

            messages.success(request, "¡Gaide está diseñando tu clase! Espera un momento.")
            return redirect('refinamientos_view', pk=planeacion.id) 
    else:
        form = CreacionEstructuraPlaneacionClaseGaideForm()

    return render(request, 'planeacion_de_clases_pags/formulario_ceacion_estructura_clase_gaide.html', {'form': form})

@login_required
def refinamientos_view(request, pk):
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk, autor=request.user)
    if planeacion.contenido_generado and "ERROR_IA" in planeacion.contenido_generado:
        messages.error(request, "Hubo un error con la IA. Por favor intenta de nuevo.")
    return render(request, 'planeacion_de_clases_pags/refinamientos_pag.html', {'planeacion': planeacion})

@login_required
def verificar_estado_ia(request, pk):
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk, autor=request.user)
    contenido = planeacion.contenido_generado
    return JsonResponse({
        'finalizado': bool(contenido),
        'error': "ERROR_IA" in (contenido or "")
    })