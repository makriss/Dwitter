from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.db import models
from Dwitter import settings

User = get_user_model()


# Create your models here.


class Dweets(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE, db_column='user_id')
    dweet = models.CharField(max_length=140)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ['-creation_timestamp']

    def __str__(self):
        return self.dweet

    def get_time_difference(self):
        difference = datetime.now(timezone.utc) - self.creation_timestamp
        if difference.days:
            return str(difference.days) + ' days'
        else:
            hours = difference.seconds / (60 * 60)
            if hours > 1:
                return str(hours) + ' hours'
            else:
                minutes = difference.seconds / 60
                if minutes > 1:
                    return str(minutes) + ' minutes'

        return str(difference.seconds) + ' seconds'

    @property
    def time_property(self):
        return self.get_time_difference()


class Comments(models.Model):
    dweet_id = models.ForeignKey('Dweets', on_delete=models.CASCADE, db_column='dweet_id')
    comment = models.TextField(default="")
    user_id = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, db_column='user_id')
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Likes(models.Model):
    dweet_id = models.ForeignKey('Dweets', on_delete=models.CASCADE, db_column="dweet_id")
    liked_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)
