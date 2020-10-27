"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from category.routers import main_router as category_router
from product.routers import main_router as product_router

schema_view = get_schema_view(
    openapi.Info(
        title="TechStartPro API",
        default_version='v1',
        description="An API that provides Products and Categories management.",
        terms_of_service="#",
        contact=openapi.Contact(email="abreumatheus@icloud.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.registry.extend(category_router.registry)
router.registry.extend(product_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/', include(router.urls)),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'', schema_view.with_ui('redoc', cache_timeout=0), name='Documentation'),
]
