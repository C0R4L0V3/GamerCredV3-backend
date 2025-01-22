from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'date_joined']

class ProfileSerializer(serializers.ModelSerializer):
    account = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1

    
