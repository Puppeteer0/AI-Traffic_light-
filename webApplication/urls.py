"""webApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from Users import urls as users_urls
from Files import urls as files_urls
from video import urls as video_urls
from django.views.generic.base import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(users_urls)),
    path('file/', include(files_urls)),
    path('video/', include(video_urls)),
    path('', TemplateView.as_view(template_name="index.html")),
    path('home/chat', TemplateView.as_view(template_name="index.html")),
    path('home/map', TemplateView.as_view(template_name="index.html")),
    path('home/file', TemplateView.as_view(template_name="index.html")),
    path('home/analyze', TemplateView.as_view(template_name="index.html")),
    path('login', TemplateView.as_view(template_name="index.html")),
]
