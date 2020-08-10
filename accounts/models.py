from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=True)
    # photo = models.ImageField(blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name + " ({})".format(self.username)

    @property
    def fullname(self):
        return self.first_name + ' ' + self.last_name
