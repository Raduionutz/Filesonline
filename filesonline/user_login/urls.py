from django.urls import path
from django.contrib.auth.views import logout_then_login
from . import views

# SET THE NAMESPACE!
app_name = 'user_login'


urlpatterns = [
    path('register/', views.register, name='register'),
    # path('index/', views.index, name='index'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.user_logout, name='logout'),
]
