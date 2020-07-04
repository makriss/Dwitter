from django.contrib.auth import get_user_model
from django.db.models import F, Value, Count, Case, When, BooleanField, OuterRef, Exists
from django.db.models.functions import Concat
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Dweets, Likes
from profiles.models import Profile


def login_user(request):
    return render(request, "login.html")


def landing_page(request):
    return render(request, "homepage.html")


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def get_homepage_feed(request):
    # users_followed = Profile.get_profile(request.user.id).get_followed_users()
    u = Profile.get_profile(request.user.id)
    users_followed = u.follow_to.all().values('user') | Profile.objects.filter(user=u.user).values("user")
    current_user_liked_query = Likes.objects.filter(
        dweet_id=OuterRef('pk'), liked_by=request.user
    )
    dweets = Dweets.objects.filter(user_id__in=users_followed) \
        .only('dweet', 'user_id', 'creation_timestamp') \
        .annotate(username=F("user_id__username"),
                  fullname=Concat('user_id__first_name', Value(' '), 'user_id__last_name'),
                  likes_count=Count('likes'), comments_count=Count('comments'),
                  current_user_liked=Exists(current_user_liked_query)
                  ) \
        .order_by('-creation_timestamp')

    # d = [{d.dweet, d.time_property} for d in dweets]
    # for dweet in dweets:
    #     dweet_object = list(dweet)
    #     dweet['creation_timestamp'] = dweet.get_time_difference()
    return Response(dweets.values())
