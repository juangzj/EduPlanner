from .usuarioUrls import urlpatterns as usuario_urls
from .sesionUrls import urlpatterns as sesion_urls

urlpatterns = usuario_urls + sesion_urls
