"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.shortcuts import redirect
from core import settings


def redirect_to_honeykitchen(request):
    return redirect('shop:index')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_honeykitchen, name='root'),
    path('honeykitchen/', include('shop.urls', namespace = 'shop')),
    path('users/', include('users.urls', namespace = 'users')),
    # path('social-auth/', include('social_django.urls', namespace = 'social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
