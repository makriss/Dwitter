from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('post-dweet', views.add_dweet, name="post_dweet"),
    path('edit-dweet', views.edit_dweet, name="edit_dweet"),
    path('post-comment', views.add_comment, name="add_comment"),
    path('edit-comment', views.edit_comment, name="edit_comment"),
    path('like-dweet', views.like_dweet, name="like_dweet"),
]
