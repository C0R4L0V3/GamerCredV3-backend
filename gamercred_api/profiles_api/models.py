from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.CharField(max_length=600, default='https://i.imgur.com/lHubf1C.jpeg')
    steam_id = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.account.username