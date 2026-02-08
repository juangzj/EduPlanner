from django.shortcuts import render, redirect

def landing_page_view(request):
    # Si ya inició sesión, lo mandamos al panel de inicio real
    if request.user.is_authenticated:
        return redirect('principal') 
    
    return render(request, "landing.html")