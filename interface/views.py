import json
from datetime import time, datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Value, Count, Case, When, BooleanField, OuterRef, Exists
from django.db.models.functions import Concat
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from api.models import Dweets, Likes, Comments
from profiles.models import Profile
from utility.functions import get_time_difference


def login_user(request):
    return render(request, "login.html")


def landing_page(request):
    return render(request, "homepage.html")


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def view_dweet(request, username, dweet_id):
    if request.method == "GET":
        return render(request, "comments-view.html")
    else:
        comments_object = fetch_comments(request, username, dweet_id)
        time_str = comments_object['dweet_info']['creation_timestamp']
        # time_str = datetime.datetime.strptime(time_str, '%m/%d/%Y')
        comments_object['dweet_info']['date'] = time_str.strftime("%d %b, %Y")
        comments_object['dweet_info']['time'] = time_str.strftime("%I:%M %p")
        comments_object['dweet_info']['creation_timestamp'] = get_time_difference(time_str)

        for comment in comments_object['comments_list']:
            comment["creation_timestamp"] = get_time_difference(comment["creation_timestamp"])

        return Response(comments_object)


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
        .values('id', 'dweet', 'user_id', 'creation_timestamp') \
        .annotate(username=F("user_id__username"),
                  fullname=Concat('user_id__first_name', Value(' '), 'user_id__last_name'),
                  likes_count=Count('likes'), comments_count=Count('comments'),
                  current_user_liked=Exists(current_user_liked_query)
                  ) \
        .order_by('-creation_timestamp')

    for d in dweets:
        d['creation_timestamp'] = get_time_difference(d['creation_timestamp'])

    return Response(dweets)


def fetch_comments(request, username, dweet_id):
    resp = {}
    try:
        current_user_liked_query = Likes.objects.filter(
            dweet_id=OuterRef('pk'), liked_by=request.user
        )
        dweet_info = Dweets.objects.filter(id=dweet_id, user_id__username=username) \
            .annotate(fullname=Concat('user_id__first_name', Value(' '), 'user_id__last_name'),
                      likes_count=Count('likes'), comments_count=Count('comments'),
                      current_user_liked=Exists(current_user_liked_query), username=F("user_id__username")
                      )
        comments_list = Comments.objects.filter(dweet_id=dweet_id) \
            .values("id", "comment", "user_id", "creation_timestamp") \
            .annotate(fullname=Concat('user_id__first_name', Value(' '), 'user_id__last_name'),
                      username=F("user_id__username")) \
            .order_by("creation_timestamp")

        resp['status'] = HTTP_200_OK
        resp['dweet_info'] = dweet_info.values()[0]
        resp['comments_list'] = comments_list
    except ObjectDoesNotExist:
        resp['status'] = HTTP_404_NOT_FOUND
    except Exception as e:
        print("exception occured----------------->", e)
        resp['status'] = HTTP_500_INTERNAL_SERVER_ERROR

    return resp
