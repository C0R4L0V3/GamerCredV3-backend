from django.contrib.auth.models import AbstractUser, BaseUserManager
from profiles_api.models import Profile
from django.db import models

# Create your models here.
# class CustomUser(AbstractUser):
#     pass
#         profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.username
    