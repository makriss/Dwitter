from django.urls import path
from django.views.generic import RedirectView

from interface import views

app_name = "home"

urlpatterns = [
    # path('logout', av.logout_user, name="logout_user"),
    path('home', views.landing_page, name="homepage"),
    path('get-feed', views.get_homepage_feed, name="get_feed"),
    path('<str:username>/status/<int:dweet_id>', views.view_dweet, name="view_dweet"),
    path('get-comments-list', views.fetch_comments),
    path('', RedirectView.as_view(url='home'), name='go-to-home')

]
