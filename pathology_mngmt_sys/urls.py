"""pathology_mngmt_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from lab.views import TakeOrder
from django.conf import settings
from django.conf.urls.static import static
from lab.views import UserLogin

urlpatterns = [
    path("",UserLogin.as_view(),name="login_global"),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    re_path(r'filer/', include('filer.urls')),
    path("lab/",include("lab.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

