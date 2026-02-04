from django.db import models
from django.conf import settings


class ComentarioPlaneacion(models.Model):
    planeacion = models.ForeignKey(
        "planeaciones_de_clases.PlaneacionClaseGaide",
        on_delete=models.CASCADE,
        related_name="comentarios"
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comentarios_planeacion"
    )

    contenido = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor} en {self.planeacion}"

    class Meta:
        db_table = "comentarios_planeacion"
        indexes = [
            models.Index(
                fields=["planeacion"],
                name="idx_comentarios_planeacion"
            ),
        ]
