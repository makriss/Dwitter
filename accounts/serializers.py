from django.contrib.auth import get_user_model
from rest_framework import serializers

from Dwitter.constants import DEFAULT_PROFILE_PIC
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]

    @property
    def get_data(self, *args):
        data = self.data
        data["fullname"] = self.instance.fullname
        data["profile_photo"] = self.instance.profile.profile_photo or DEFAULT_PROFILE_PIC
        return data


class CurrentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profile_photo']


class CurrentUserSerializer(serializers.ModelSerializer):
    profile = CurrentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "profile")
