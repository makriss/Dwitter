from django.contrib import admin
from django.urls import path
from interface import views
from accounts import views as av

urlpatterns = [
    # path('logout', av.logout_user, name="logout_user"),
    path('home', views.landing_page, name="home"),
    path('get-feed', views.get_homepage_feed, name="get_feed"),

]
