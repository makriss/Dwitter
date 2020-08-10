from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from Dwitter import settings

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=160, blank=True)
    profile_photo = models.ImageField(blank=True, null=True)
    followers = models.ManyToManyField("self", through="Relationship", related_name="follow_to",
                                       through_fields=("user_followed", "followed_by"), symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

    def get_followers(self):
        return self.followers.all()

    def get_followed_users(self):
        return self.follow_to.all().values('user')

    def check_if_following(self, username):
        try:
            following_user = self.follow_to.get(user__username=username)
        except ObjectDoesNotExist:
            following_user = False

        return following_user

    def get_followers_count(self):
        return self.followers.count()

    @staticmethod
    def get_profile(user_object):
        return Profile.objects.get(user=user_object)

    @staticmethod
    def get_profile_from_username(username):
        user = User.objects.get(username=username)
        return user.profile

    def follow_user(self, to_follow_username):
        profile = Profile.get_profile_from_username(to_follow_username)
        try:
            rel = Relationship.objects.create(user_followed=profile,
                                              followed_by=self)
            rel = True
        except Exception as e:
            rel = Relationship.objects.get(user_followed=profile,
                                           followed_by=self)
            rel.delete()
            rel = False

        return rel

    # def follow(self, user_profile):


class Relationship(models.Model):
    user_followed = models.ForeignKey("Profile", related_name="followed",
                                      on_delete=models.CASCADE, db_column="user_followed")
    followed_by = models.ForeignKey("Profile", related_name="follower",
                                    on_delete=models.CASCADE, db_column="followed_by")
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_followed", "followed_by"],
                                    name="single follow")
        ]
