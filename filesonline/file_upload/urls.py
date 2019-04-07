from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'file_upload'

urlpatterns = [
    path('file/', views.upload_file),
    path('', views.upload_index),
]