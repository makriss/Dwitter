from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Value, Count, Exists, OuterRef
from django.db.models.functions import Concat

from Dwitter import settings
from utility.functions import get_time_difference

User = get_user_model()


class Dweets(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column='user_id')
    dweet = models.CharField(max_length=140)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ['-creation_timestamp']

    def __str__(self):
        return self.dweet

    @property
    def get_readable_time(self):
        return get_time_difference(self.creation_timestamp)

    @staticmethod
    def get_dweets_of_user(username):
        return Dweets.objects.filter(user_id__username=username) \
            .order_by('-creation_timestamp')


class Comments(models.Model):
    dweet_id = models.ForeignKey('Dweets', on_delete=models.CASCADE, db_column='dweet_id')
    comment = models.TextField(default="")
    user_id = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, db_column='user_id')
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    def getCountForComment(self):
        return Comments.objects.filter(dweet_id=self.dweet_id).count()


class Likes(models.Model):
    dweet_id = models.ForeignKey('Dweets', on_delete=models.CASCADE, db_column="dweet_id")
    liked_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_dweets_liked_by_user(username):
        user_liked_query = Likes.objects.filter(
            dweet_id=OuterRef('pk'), liked_by__username=username
        )
        return Likes.objects.filter(liked_by__username=username) \
            .annotate(dweet=F("dweet_id__dweet"), username=F("dweet_id__user_id__username"),
                      fullname=Concat('dweet_id__user_id__first_name', Value(' '), 'dweet_id__user_id__last_name'),
                      likes_count=Count('dweet.likes_set.all()'),
                      # current_user_liked=Exists(user_liked_query)
                      ) .select_related('dweet_id').likes_set.all()\
            .order_by('-last_update')
