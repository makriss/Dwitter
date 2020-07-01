from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED

from api.views import failed_object
from profiles.models import Profile


def create_minimal_profile(request):
    Profile.objects.create(user=request)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    response_object = {}
    try:
        follow_username = request.data['follow_username']
        request.user.profile.follow_user(follow_username)
        response_object.update({'status': HTTP_201_CREATED})

    except Exception as e:
        print("----------Exception occured--------", e)
        response_object = failed_object(HTTP_500_INTERNAL_SERVER_ERROR, e)

    return Response(response_object)
