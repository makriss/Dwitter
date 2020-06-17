from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

import accounts.serializers as ser
# Create your views here.

@api_view(['POST',])
def RegisterUser(request):
    print("Registering user....",request.data)
    if request.method == "POST":
        serializer = ser.RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            print("account:",account)
            data["response"] = "Successfully registered"
        else:
            data = serializer.errors
    return Response(data)

@api_view(['POST',])
def TokenLogin(request):
    if request.method == "POST":
        data = {}
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                token = get_object_or_404(Token, user=user)
                # print("Token retrieved:",token)
            except:
                token = Token.objects.create(user=user)
                # print("Token created:",token)
            data.update({'token':token.key})
        else:
            data.update({'msg':"Login failed!"})
    return Response(data)