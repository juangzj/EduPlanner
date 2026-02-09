from django.contrib import admin

# Register your models here.
from .models.comentarioPlaneacion import ComentarioPlaneacion
from .models.likePlaneacion import LikePlaneacion


admin.site.register(ComentarioPlaneacion)
admin.site.register(LikePlaneacion)