from django.contrib import admin
from django.urls import path,include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Garage Management API",
        default_version='v1',
        description="Documentation de l'API pour la gestion du garage",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/rgh/', include('ressources_humaine.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/interventions/', include('interventions.urls')),
    path('api/stock/', include('stock.urls')),
    path('api/tresorerie/', include('tresorerie.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]