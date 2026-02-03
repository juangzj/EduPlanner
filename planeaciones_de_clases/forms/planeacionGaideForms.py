from django import forms
from ..models.planeacionClaseGaide import PlaneacionClaseGaide  

class CreacionEstructuraPlaneacionClaseGaideForm(forms.ModelForm):
    class Meta:
        model = PlaneacionClaseGaide
        fields = [
            'grado', 
            'area', 
            'tema', 
            'competencia', 
            'objetivo_aprendizaje', 
            'duracion_clase', 
            'nivel_grupo', 
            'informacion_adicional'
        ]
        
        # Widgets actualizados para soportar los campos seleccionables
        widgets = {
            'grado': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'tema': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: La Célula'}),
            'competencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '¿Qué competencia desarrollarán?'}),
            'objetivo_aprendizaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '¿Qué aprenderá el estudiante?'}),
            'duracion_clase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 90 minutos'}),
            'nivel_grupo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Principiante / Avanzado'}),
            'informacion_adicional': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contexto extra del grupo o recursos...'}),
        }
        
        labels = {
            'grado': 'Grado Académico',
            'area': 'Área de Conocimiento',
            'tema': 'Tema Principal',
            'competencia': 'Competencia a Desarrollar',
            'objetivo_aprendizaje': 'Objetivo de Aprendizaje',
            'duracion_clase': 'Duración de la Clase',
            'nivel_grupo': 'Nivel del Grupo',
            'informacion_adicional': 'Información Adicional (Opcional)',
        }