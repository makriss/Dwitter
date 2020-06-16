from rest_framework import serializers

from api.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']

    def create(self, validated_data):
        u = {
            'username' : validated_data['username'],
            'password' : validated_data['password']
        }
        print("User data:",u)
        u = User.objects.create_user(u)
        u.save()
        return u