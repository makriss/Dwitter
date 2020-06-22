from django.contrib import admin
from django.urls import path, include
from accounts import views
from rest_framework.authtoken import views as v

urlpatterns = [
   path('register',views.RegisterUser,name="register"),
   path('login',views.TokenLogin,name="login"),
   path('fetch-token',v.obtain_auth_token,name="get_token")
]