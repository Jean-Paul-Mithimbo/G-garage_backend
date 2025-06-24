from django.contrib import admin
from django.urls import path,include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.shortcuts import render

def api_home(request):
    return render(request, "api_home.html")

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
    path('', api_home, name='api_home'),
    path('api/auth/', include('authentication.urls')),
    path('api/rgh/', include('ressources_humaine.urls')),
    path('api/clients/', include('clients.urls')),
    path('api/interventions/', include('interventions.urls')),
    path('api/stock/', include('stock.urls')),
    path('api/tresorerie/', include('tresorerie.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()