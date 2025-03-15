"""
URL configuration for cognicursos project.

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
from rest_framework import routers
from api import views

# Configuração do router do DRF
router = routers.DefaultRouter()
# Aqui serão registradas as viewsets da API
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'configuracoes-ia', views.ConfiguracaoIAViewSet)
router.register(r'interacoes', views.InteracaoViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
