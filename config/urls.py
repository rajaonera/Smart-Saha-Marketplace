from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Smart Saha Marketplace API",
      default_version='v1',
      description="Documentation API pour le backend Marketplace",
      contact=openapi.Contact(email="contact@smartsaha.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),

    # Ajout de l'inclusion des urls marketplace
    path('', include('marketplace.urls')),  # inclut toutes les routes définies dans marketplace/urls.py

    # Swagger UI:
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Redoc UI (optionnel):
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
