from django.contrib.auth.decorators import login_required
from django.db.models import Value, Count, F
from django.db.models.functions import Concat
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED

import utility.functions as uf
from Dwitter.constants import DEFAULT_PROFILE_PIC
from interface.views import get_feed_from_db
from profiles.models import Profile
from profiles.queries import get_liked_dweets_by_profile_query


def create_minimal_profile(request):
    Profile.objects.create(user=request)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
@login_required
def follow_user(request):
    response_object = {}
    try:
        follow_username = request.data['follow_username']
        is_following = request.user.profile.follow_user(follow_username)
        response_object = uf.success_object(HTTP_201_CREATED, "following", is_following)

    except Exception as e:
        print("----------Exception occurred--------", e)
        response_object = uf.failed_object(HTTP_500_INTERNAL_SERVER_ERROR, e)

    return Response(response_object)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
@login_required
def show_profile(request, username):
    if request.method == "POST":
        response_object = {}
        username = username.strip()
        my_profile = True if username == request.user.username else False
        profile_info = Profile.objects.filter(user__username=username).values("bio", "profile_photo") \
            .annotate(username=F("user__username"), fullname=Concat('user__first_name', Value(' '), 'user__last_name'),
                      following=Count("follow_to"), followers_count=Count("followers"),
                      )
        profile_info = profile_info if len(profile_info) else [{}]
        profile_info[0]['profile_photo'] = DEFAULT_PROFILE_PIC if not profile_info[0]['profile_photo'] else profile_info[0]['profile_photo']

        response_object.update({"profile_info": profile_info[0]})
        if not my_profile:
            following_check = request.user.profile.check_if_following(username)
            following = True if following_check else False
            response_object.update({"following": following})
        else:
            response_object.update({"my_profile": my_profile})

        # fetching dweets of user
        response_object['user_dweets'] = get_feed_from_db(request, username)

        # fetching all dweets liked by user
        query = get_liked_dweets_by_profile_query
        query = query.replace('__CURRENT_USER_ID__', str(request.user.id)).replace('__PROFILE_USERNAME__', username)
        user_liked_dweets = uf.dict_fetch_all(query)
        for dweet in user_liked_dweets:
            dweet['creation_timestamp'] = uf.get_time_difference(dweet['creation_timestamp'])
            dweet['profile_photo'] = DEFAULT_PROFILE_PIC if not dweet['profile_photo'] else dweet['profile_photo']
        response_object['liked_dweets'] = user_liked_dweets

        return Response(response_object)

    else:
        return render(request, 'profile-page.html', )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@login_required
def edit_profile(request, username):
    print(request.data)