from django.contrib import admin
from django.urls import path, include

import api
from profiles import views

urlpatterns = [
    path('follow-user', views.follow_user, name="follow_user"),

]