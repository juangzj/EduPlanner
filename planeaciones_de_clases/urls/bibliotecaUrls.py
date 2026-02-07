from django.urls import path
from ..views import  bibliotecaViews

urlpatterns = [

 # URL de redireccionamiento a la vista biblioteca.html
    path(
        "biblioteca/", 
        bibliotecaViews.biblioteca_view, 
        name="biblioteca"
    ),
    path("biblioteca/editar/<int:pk>/", bibliotecaViews.editar_planeacion, name="editar_planeacion"),
    path("biblioteca/eliminar/<int:pk>/", bibliotecaViews.eliminar_planeacion, name="eliminar_planeacion"),
]