from django.urls import path
from Files import views


urlpatterns = [
    path('upload_files', views.upload_files),
    path('show_files', views.show_files),
    path('dowload_files', views.download_files),
    path('delete_file', views.delete_file)
]
