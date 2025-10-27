from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.urls import path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls", namespace="core")),
    path("api/", include("core.api_urls")),
     # Rutas de autenticación
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
   
   
   # Ruta para el esquema OpenAPI (solo JSON)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Documentación visual Swagger (usa el JSON anterior)
path("api/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)