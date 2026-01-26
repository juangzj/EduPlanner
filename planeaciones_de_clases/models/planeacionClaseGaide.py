from django.db import models
from django.conf import settings


class PlaneacionClaseGaide(models.Model):
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planeaciones'
    )

    # ===============================
    # Metadatos pedagogicos
    # ===============================
    grado = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    tema = models.CharField(max_length=255)
    competencia = models.TextField()
    objetivo_aprendizaje = models.TextField()
    duracion_clase = models.CharField(max_length=100)
    nivel_grupo = models.CharField(max_length=100)
    informacion_adicional = models.TextField(blank=True, null=True)

    # ===============================
    # Resultado final IA
    # ===============================
    contenido_generado = models.TextField(blank=True, null=True)

    # ===============================
    # Estructura GAIDE
    # ===============================
    fase_guide_json = models.JSONField(blank=True, null=True)

    # ===============================
    # Historial de IA
    # ===============================
    historial_refinamientos = models.JSONField(blank=True, null=True)

    # ===============================
    # Control de refinamientos
    # ===============================
    intentos_refinamiento = models.IntegerField(default=0)

    # ===============================
    # Estados de la planeacion
    # ===============================
    publicada = models.BooleanField(default=False)
    planeacion_finalizada = models.BooleanField(default=False)

    # ===============================
    # Fechas
    # ===============================
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tema} - {self.grado}"

    class Meta:
        db_table = "planeaciones_de_clases_planeacionclasegaide"
        indexes = [
            models.Index(fields=["autor"], name="idx_planeacion_autor")
        ]
