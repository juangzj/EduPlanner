import django_filters
from ..models import PlaneacionClaseGaide

class PlaneacionClaseGaideBibliotecaFiltro(django_filters.FilterSet):
    # Filtro de rango para fecha de creación (Desde - Hasta)
    fecha_desde = django_filters.DateFilter(
        field_name='fecha_creacion', 
        lookup_expr='gte',
        label='Fecha creación desde'
    )
    fecha_hasta = django_filters.DateFilter(
        field_name='fecha_creacion', 
        lookup_expr='lte',
        label='Fecha creación hasta'
    )

    class Meta:
        model = PlaneacionClaseGaide
        fields = {
            'grado': ['exact'],
            'area': ['exact'],
            'publicada': ['exact'],
            'planeacion_finalizada': ['exact'],
        }