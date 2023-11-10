from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# class ThirdPartyToken(models.Model):
#     name = models.CharField(max_length=255)
#     token = models.TextField(max_length=1024)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name