from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from Dwitter import settings
from accounts.models import User
from api.models import Dweets, Comments, Likes


class DweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dweets
        fields = ["dweet"]

    def create(self, validated_data):
        return Dweets.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.dweet = validated_data.get('dweet', instance.dweet)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ["dweet_id", "comment"]

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ["dweet_id"]

    def save(self, **kwargs):
        dweet = self.validated_data["dweet_id"]
        user = kwargs['user_id']

        if self.checkIfLiked(user):  # delete the table entry
            like = Likes.objects.get(dweet_id=dweet.id, liked_by=user.id)
            like.delete()
            current_user_liked = False
        else:  # create an entry
            like_object = Likes.objects.create(dweet_id=dweet, liked_by=user)
            current_user_liked = True

        total_likes = Likes.objects.filter(dweet_id=dweet.id).count()

        return {"current_user_liked": current_user_liked, "total_likes": total_likes}

    def checkIfLiked(self, user):
        dweet = self.validated_data["dweet_id"]
        try:
            get_object_or_404(Likes, dweet_id=dweet.id, liked_by=user.id)
            # if interpreter reaches next lines, means object in table exists
            liked = True
        except Http404:
            liked = False

        return liked
