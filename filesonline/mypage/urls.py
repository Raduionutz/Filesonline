from django.urls import path
from . import views

app_name = 'mypage'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('delete_file', views.DeleteFileView.as_view(), name='delete_file'),
]