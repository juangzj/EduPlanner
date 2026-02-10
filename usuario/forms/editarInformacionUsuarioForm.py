# forms.py
from django import forms
from ..models import UsuarioDocente

class EditarInformacionUsuarioForm(forms.ModelForm):
    class Meta:
        model = UsuarioDocente
        # REVISA ESTA LISTA: Deben estar los 7 campos
        fields = [
            'gmail', 
            'primer_nombre', 
            'segundo_nombre', 
            'primer_apellido', 
            'segundo_apellido', 
            'apodo', 
            'fecha_nacimiento'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditarInformacionUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['gmail'].disabled = True