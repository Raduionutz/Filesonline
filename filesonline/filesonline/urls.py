"""filesonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from mypage.views import RedirectHome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(('user_login.urls', 'user_login'), namespace='user_login')),
    path('upload/', include(('file_upload.urls', 'file_upload'), namespace='file_upload')),
    path('me/', include(('mypage.urls', 'mypage'), namespace='mypage')),
    path('', RedirectHome.as_view(), name='home')
]
