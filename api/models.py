from django.contrib.auth import get_user_model
from django.db import models
from Dwitter import settings

User = get_user_model()

# Create your models here.


class Dweets(models.Model):
    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    dweet = models.CharField(max_length=140)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering: ['-creation_timestamp']

    def __str__(self):
        return self.dweet


class Comments(models.Model):
    dweet_id = models.ForeignKey('Dweets', on_delete=models.CASCADE)
    comment = models.TextField(default="")
    user_id = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class Likes(models.Model):
    dweet_id = models.ForeignKey('Dweets', on_delete=models.CASCADE)
    liked_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now=True)

