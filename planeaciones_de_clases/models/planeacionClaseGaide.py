from django.db import models
from django.conf import settings

class PlaneacionClaseGaide(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='planeaciones'
    )
    
    #  campos solicitados
    grado = models.CharField(max_length=50)
    area = models.CharField(max_length=100) # Ej: Ciencias Naturales
    tema = models.CharField(max_length=255)
    competencia = models.TextField()
    objetivo_aprendizaje = models.TextField()
    duracion_clase = models.CharField(max_length=100) # Ej: 2 horas o 90 min
    nivel_grupo = models.CharField(max_length=100) # Ej: Básico, Intermedio
    informacion_adicional = models.TextField(blank=True, null=True)

    # Campos técnicos que mantendremos para la IA
    contenido_generado = models.TextField(blank=True, null=True)
    fase_guide_json = models.JSONField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    publicada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tema} - {self.grado}"