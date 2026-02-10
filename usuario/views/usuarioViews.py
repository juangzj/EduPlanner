from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ..forms import usuario_form
from django.contrib.auth.decorators import login_required
from ..forms.editarInformacionUsuarioForm import EditarInformacionUsuarioForm 



def registrar_usuario_view(request):
    if request.method == "POST":
        form = usuario_form.RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(
                request, "✅ El usuario se creó correctamente. Bienvenido/a."
            )
            return redirect("principal")
        else:
            messages.error(
                request,
                "❌ El formulario contiene errores. Revisa los campos marcados.",
            )
    else:
        form = usuario_form.RegistroForm()

    return render(request, "registrar_usuario_pag.html", {"form": form})


@login_required
def editar_perfil(request):
    usuario = request.user
    
    if request.method == 'POST':
        form = EditarInformacionUsuarioForm(request.POST, instance=usuario)
        
        # --- VERIFICACIÓN EN CONSOLA ---
        print("\n" + "="*20)
        print("DATOS RECIBIDOS (POST):")
        for key, value in request.POST.items():
            print(f"{key}: {value}")
        print("="*20 + "\n")
        # -------------------------------

        if form.is_valid():
            # También puedes imprimir los datos limpios después de validar
            print("Datos validados correctamente:", form.cleaned_data)
            
            form.save()
            messages.success(request, "¡Perfil actualizado con éxito!")
            return redirect('editar_perfil')
        else:
            # En caso de error, imprimimos qué falló
            print("Errores del formulario:", form.errors.as_data())
            messages.error(request, "Por favor, corrige los errores.")
    else:
        form = EditarInformacionUsuarioForm(instance=usuario)
    
    return render(request, 'editar_perfil.html', {'form': form})