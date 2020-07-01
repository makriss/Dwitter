from django.contrib.auth import get_user_model
from rest_framework import serializers

from profiles.models import Profile

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        u = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=u)

        return u
