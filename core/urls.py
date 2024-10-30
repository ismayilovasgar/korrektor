"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
schema_view = get_schema_view(
    openapi.Info(
        title="Korrektor API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # İzinler burada ayarlanır
    authentication_classes=[],  # JWT Authentication burada ayarlanır
)

urlpatterns = [
    #
    # 
    ## admin panel
    path("admin/", admin.site.urls),
    #
    # 
    ## account applications
    path("api/accounts/", include("accounts.api.urls")),
    # 
    # 
    ## create contact form
    path("api/contact/", include("contact.api.urls")),
    #
    # 
    ## corrections
    path("api/corrections/", include("corrections.api.urls")),  
    # 
    # 
    ## meta_manager
    path('api/meta/', include('meta.api.urls')),  
    # 
    # 
    ## testmonials
    path('api/testimonials/', include('testimonials.api.urls')), 
    # 
    # 
    ## OpenAPI şeması
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    #
    # 
    ## Swagger dokümantasyonu
    path("swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/",schema_view.with_ui("swagger", cache_timeout=0),name="schema-swagger-ui"),
    # path("api/schema/swagger-ui/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    #
    # 
    ## rest auth google
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/google/", include("allauth.socialaccount.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
