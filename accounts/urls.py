from django.contrib import admin
from django.urls import path, include
from accounts import views
from rest_framework.authtoken import views as v

app_name = "accounts"

urlpatterns = [
    path('register', views.RegisterUser, name="register"),
    path('token_login', views.TokenLogin, name="token_login"),
    path('fetch-token', v.obtain_auth_token, name="get_token"),
    path('login', views.login_user, name="login_user"),
    path('logout', views.logout_user, name="user_logout"),
    path('current_user', views.get_loggedin_user),

]
