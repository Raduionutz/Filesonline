from django.urls import path, re_path
from . import views

app_name = 'mypage'

urlpatterns = [
    re_path(r'folder?/(?P<path>.*)', views.MainPage.as_view(), name='main_page'),
    path('delete_file', views.DeleteFile.as_view(), name='delete_file'),
    path('download_file', views.DownloadFile.as_view(), name='download_file'),
    path('share_file', views.ShareFile.as_view(), name='share_file'),
    path('move_file', views.MoveSharedFile.as_view(), name='move_file'),
    path('encrypt_file', views.EncryptFile.as_view(), name='encrypt_file'),
    path('decrypt_file', views.DecryptFile.as_view(), name='decrypt_file'),
    path('dec-download_file', views.DecryptDownloadFile.as_view(), name='dec-download_file'),
    # path('/folder/<string:path>', views.MainPage.as_view(), name='main_page'),
]
