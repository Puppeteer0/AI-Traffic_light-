from django.urls import path
from video import views

urlpatterns = [
    path('upload_files', views.upload_files),
    path('show_files', views.show_files),
    path('download_files', views.download_files),
    path('delete_file', views.delete_file),
    path('get_video_detail', views.get_video_detail),
    path('select_video_detail', views.select_video_detail)
]
