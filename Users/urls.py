from django.urls import path
import Users.views as views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('check', views.check_nickname),
    path('get_personal_info', views.get_personal_info),
    path('upload_avatar', views.upload_avatar),
    path('get_address', views.get_address),
    path('get_spot_info', views.get_spot_info),
    path('get_routes', views.get_routes),
    path('get_avatar', views.get_avatar)
]
