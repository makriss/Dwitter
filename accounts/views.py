from django.shortcuts import render
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