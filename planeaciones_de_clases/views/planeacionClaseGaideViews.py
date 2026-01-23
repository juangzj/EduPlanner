from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Importamos específicamente la clase del formulario desde su archivo
from ..forms.planeacionGaideForms import CreacionEstructuraPlaneacionClaseGaideForm

@login_required 
def crear_planeacion_clase_gaide(request):
    if request.method == 'POST':
        form = CreacionEstructuraPlaneacionClaseGaideForm(request.POST)
        
        if form.is_valid():
            planeacion = form.save(commit=False)
            planeacion.autor = request.user
            # Aquí podrías añadir lógica para generar contenido con IA antes del save()
            planeacion.save()
            
            messages.success(request, "¡Estructura de planeación creada con éxito!")
            # Asegúrate de tener esta URL nombrada en tu urls.py
            return redirect('lista_planeaciones') 
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CreacionEstructuraPlaneacionClaseGaideForm()

    return render(request, 'planeacion_de_clases_pags/formulario_ceacion_estructura_clase_gaide.html', {
        'form': form
    })