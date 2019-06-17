from django.urls import path, re_path
from . import views

app_name = 'mypage'

urlpatterns = [
    re_path(r'folder/(?P<path>.*)', views.MainPage.as_view(), name='main_page'),
    path('vault', views.VaultPage.as_view(), name='vault_page'),
    path('delete_file', views.DeleteFile.as_view(), name='delete_file'),
    path('download_file', views.DownloadFile.as_view(), name='download_file'),
    path('share_file', views.ShareFile.as_view(), name='share_file'),
    path('move_file', views.MoveSharedFile.as_view(), name='move_file'),
    path('copy_file', views.CopyFile.as_view(), name='copy_file'),
    path('encrypt_file', views.EncryptFile.as_view(), name='encrypt_file'),
    path('decrypt_file', views.DecryptFile.as_view(), name='decrypt_file'),
    path('dec-download_file', views.DecryptDownloadFile.as_view(), name='dec-download_file'),
    path('make_dir', views.MakeDirectory.as_view(), name='make_dir'),
    path('change_dir', views.ChangeDirectory.as_view(), name='change_dir'),
    path('delete_dir', views.DeleteDirectory.as_view(), name='delete_dir'),
    path('move_to_dir', views.MoveToDirectory.as_view(), name='move_to_dir'),
    path('unshare_file', views.UnshareFile.as_view(), name='unshare_file'),
    path('hide_file', views.HideFile.as_view(), name='hide_file'),
    path('unhide_file', views.UnhideFile.as_view(), name='unhide_file'),
    path('enter_vault', views.EnterVaultKey.as_view(), name='enter_vault'),
]
