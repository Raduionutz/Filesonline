import os

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from filesonline.settings import DEBUG, MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_DIR

from mypage.views import RedirectHome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(('user_login.urls', 'user_login'), namespace='user_login')),
    path('upload/', include(('file_upload.urls', 'file_upload'), namespace='file_upload')),
    path('me/', include(('mypage.urls', 'mypage'), namespace='mypage')),
    path('', RedirectHome.as_view(), name='home')
]

urlpatterns += static(MEDIA_URL + 'profile_pics/', document_root=os.path.join(MEDIA_ROOT, 'profile_pics'))
