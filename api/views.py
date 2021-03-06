from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, \
    HTTP_400_BAD_REQUEST

from api.models import Dweets, Likes
from api.serializers import DweetSerializer, CommentSerializer, LikeSerializer
from profiles.models import Profile
from utility.functions import get_time_difference, failed_object


@api_view(['POST', ])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_dweet(request):
    response_object = {}
    if request.method == "POST":
        # request.data.user_id = request.user.pk
        dweet_serializer = DweetSerializer(data=request.data)
        if dweet_serializer.is_valid():
            dweet_object = dweet_serializer.save(user_id=request.user)
            dweet = {'id': dweet_object.id, 'dweet': dweet_object.dweet}
            response_object.update({'status': HTTP_201_CREATED})
            response_object.update({'dweet': dweet})
        else:
            response_object = failed_object(HTTP_400_BAD_REQUEST, dweet_serializer.errors)
        return Response(response_object)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def edit_dweet(request):
    response_object = {}
    if request.method == "POST":
        try:
            dweet = Dweets.objects.get(id=request.data['id'])

            # validating if editor of dweet is same as creator of dweet
            if request.user.id != dweet.user_id.id:
                return Response({"status": HTTP_401_UNAUTHORIZED})

            dweet_serializer = DweetSerializer(dweet, data=request.data)
            if dweet_serializer.is_valid():
                dweet_object = dweet_serializer.save()
                dweet = {'id': dweet_object.id, 'dweet': dweet_object.dweet}

                response_object.update({'status': HTTP_201_CREATED})
                response_object.update({'dweet': dweet})

            else:
                response_object = failed_object(HTTP_400_BAD_REQUEST, dweet_serializer.errors)

        except Exception as e:
            print("----------Exception occured--------", e)
            response_object = failed_object(HTTP_500_INTERNAL_SERVER_ERROR, e)

        return Response(response_object)


# @api_view(['POST', ])
# @permission_classes([IsAuthenticated])
def get_dweet(request):
    try:
        dweet = get_object_or_404(Dweets, id=request.data['dweet_id'])
    except Http404:
        print("No Dweet exist with dweet id:", request.data['dweet_id'])
        dweet = False
    return Response(dweet)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def add_comment(request):
    response_object = {}
    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user_id=request.user)
            count = comment.getCountForComment()
            comment.creation_timestamp = get_time_difference(comment.creation_timestamp)
            c = comment.__dict__
            comment_data = {
                "id": comment.id,
                "comment": comment.comment,
                "username": comment.user_id.username,
                "fullname": comment.user_id.full_name,
                "creation_timestamp": comment.creation_timestamp
            }
            response_object = {
                "status": HTTP_201_CREATED,
                "total_comments": count,
                "comment": comment_data
            }
        else:
            response_object = failed_object(HTTP_400_BAD_REQUEST, serializer.errors)
    return Response(response_object)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def edit_comment(request):
    pass


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def like_dweet(request):
    """
    Likes or likes a dweet.

    :param request: <int> dweet_id
    :return: <Dictionary> {likes_count<int>, current_user_liked<Boolean>}
    """

    # request_dweet_object = {"dweet_id": request.data}
    like_serializer = LikeSerializer(data=request.data)
    if like_serializer.is_valid():
        like_object = like_serializer.save(user_id=request.user)
    else:
        like_serializer.errors
        print("-----------Errors-----------", like_serializer.errors)

    return Response(like_object)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def follow_user(request):
    """
        Likes or likes a dweet.

        :param request: <int> dweet_id
        :return: <Dictionary> {likes_count<int>, is_follower<Boolean>}
    """
    followed = request.data['user_id']
    user_id = request.user.id
    try:
        followed_object = get_object_or_404(Followers, user_id=followed)
        followers_list = followed_object.followers

        followers_list = followers_list.split(',')
        if user_id in followers_list:
            followers_list.remove(user_id)
            is_follower = False
        else:
            followers_list.append(user_id)
            is_follower = True
    except Http404:
        user = get_user(request)
        followed_object = Likes.objects.create(dweet_id=dweet.data)
        followers_list = [user_id]
        is_follower = True

    likes_count = len(followers_list)
    if not len(followers_list):
        followed_object.delete()  # removing dweet table entry if no likes
        is_follower = False
    else:
        followers_list = ",".join(followers_list)
        followed_object.liked_by = followers_list
        followed_object.save()

    return Response({"is_follower": is_follower, "likes_count": likes_count})


