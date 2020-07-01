from django.contrib import auth
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import accounts.serializers as ser
# Create your views here.
from interface.forms import LoginUserForm


# @api_view(['POST', ])
def RegisterUser(request):
    print("Registering user....", request.data)
    if request.method == "POST":
        serializer = ser.RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            print("account:", account)
            data["response"] = "Successfully registered"
        else:
            data = serializer.errors
        return Response(data)


@api_view(['POST', ])
def TokenLogin(request):
    if request.method == "POST":
        data = {}
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # try:
            #     token = get_object_or_404(Token, user=user)
            #     # print("Token retrieved:",token)
            # except:
            #     token = Token.objects.create(user=user)
            #     # print("Token created:",token)
            token = Token.objects.get_or_create(user=user)
            data.update({'token': token.key})
        else:
            data.update({'msg': "Login failed!"})
    return Response(data)


# @api_view(['POST','GET'])
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("Login success")
            return HttpResponse("<h3>Login Success!!!!</h3>")
        else:
            print("Login failed")
            # form = LoginUserForm()
    elif request.user.is_authenticated:
        print("User already AUTHENTICATED")

    return render(request, "login.html")

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_user'))