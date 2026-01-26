from django.db import models
from django.conf import settings


class LikePlaneacion(models.Model):
    planeacion = models.ForeignKey(
        "PlaneacionClaseGaide",
        on_delete=models.CASCADE,
        related_name="likes"
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_planeacion"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} -> {self.planeacion}"

    class Meta:
        db_table = "likes_planeacion"
        constraints = [
            models.UniqueConstraint(
                fields=["planeacion", "usuario"],
                name="unique_like_usuario_planeacion"
            )
        ]
