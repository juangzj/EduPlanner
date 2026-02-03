from django.db import models
from django.conf import settings

class PlaneacionClaseGaide(models.Model):
    # Definición de opciones para Grado
    GRADOS_OPCIONES = [
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('4', 'Cuarto'),
        ('5', 'Quinto'),
        ('6', 'Sexto'),
        ('7', 'Séptimo'),
        ('8', 'Octavo'),
        ('9', 'Noveno'),
        ('10', 'Décimo'),
        ('11', 'Once'),
    ]

    # Definición de opciones para Área
    AREAS_OPCIONES = [
        ('Español / Castellano', 'Español / Castellano'),
        ('Matemáticas', 'Matemáticas'),
        ('Ingles', 'Ingles'),
        ('Sociales', 'Sociales'),
        ('Ciencias Naturales', 'Ciencias Naturales'),
        ('Educación Física', 'Educación Física'),
        ('Filosofía', 'Filosofía'),
        ('Artística', 'Artística'),
        ('Ética y Valores', 'Ética y Valores'),
        ('Informática', 'Informática'),
    ]

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='planeaciones'
    )

    # ===============================
    # Metadatos pedagogicos (Campos con choices)
    # ===============================
    grado = models.CharField(
        max_length=2, 
        choices=GRADOS_OPCIONES,
        default='1'
    )
    area = models.CharField(
        max_length=100, 
        choices=AREAS_OPCIONES
    )
    
    tema = models.CharField(max_length=255)
    competencia = models.TextField()
    objetivo_aprendizaje = models.TextField()
    duracion_clase = models.CharField(max_length=100)
    nivel_grupo = models.CharField(max_length=100)
    informacion_adicional = models.TextField(blank=True, null=True)

    # ... (el resto de tus campos se mantienen igual)
    contenido_generado = models.TextField(blank=True, null=True)
    fase_guide_json = models.JSONField(blank=True, null=True)
    historial_refinamientos = models.JSONField(blank=True, null=True)
    intentos_refinamiento = models.IntegerField(default=0)
    publicada = models.BooleanField(default=False)
    planeacion_finalizada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Usamos get_grado_display() para que en el admin se vea "Primero" y no solo "1"
        return f"{self.tema} - {self.get_grado_display()} ({self.area})"

    class Meta:
        db_table = "planeaciones_de_clases_planeacionclasegaide"
        indexes = [
            models.Index(fields=["autor"], name="idx_planeacion_autor")
        ]