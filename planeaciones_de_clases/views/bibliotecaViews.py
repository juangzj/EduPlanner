from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models.planeacionClaseGaide import PlaneacionClaseGaide
from ..forms.planeacionGaideForms import CreacionEstructuraPlaneacionClaseGaideForm
from ..filtros.planeacionClaseGaideBibliotecaFiltro import PlaneacionClaseGaideBibliotecaFiltro

# --- READ: Ver lista de planeaciones ---
@login_required
def biblioteca_view(request):
    # 1. Obtenemos el queryset base (solo las del autor)
    queryset_base = PlaneacionClaseGaide.objects.filter(autor=request.user).order_by('-fecha_creacion')
    
    # 2. Inicializamos el filtro con los datos de la URL (request.GET) y el queryset
    filtro = PlaneacionClaseGaideBibliotecaFiltro(request.GET, queryset=queryset_base)
    
    # 3. El queryset filtrado está en filtro.qs
    return render(request, 'planeacion_de_clases_pags/biblioteca.html', {
        'planeaciones': filtro.qs, # Pasamos los resultados filtrados
        'filter': filtro           # Pasamos el objeto filtro para renderizar el formulario
    })

# --- UPDATE: Editar metadatos ---
@login_required
def editar_planeacion(request, pk):
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        form = CreacionEstructuraPlaneacionClaseGaideForm(request.POST, instance=planeacion)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Planeación actualizada con éxito!")
            return redirect('biblioteca')
    else:
        form = CreacionEstructuraPlaneacionClaseGaideForm(instance=planeacion)
    
    return render(request, 'componentes/editar_planeacion.html', {
        'form': form, 
        'planeacion': planeacion
    })

# --- DELETE: Eliminar planeación ---
@login_required
def eliminar_planeacion(request, pk):
    planeacion = get_object_or_404(PlaneacionClaseGaide, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        planeacion.delete()
        messages.success(request, "La planeación ha sido eliminada.")
        return redirect('biblioteca')
    
    return render(request, 'componentes/confirmar_eliminar.html', {
        'planeacion': planeacion
    })