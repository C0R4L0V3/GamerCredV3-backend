from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from .serializers import UserSerializer
from profiles_api.serializers import ProfileSerializer
from profiles_api.models import Profile


# Create your views here.

#user registration

class RegisterUserAPIView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            #create the user profile
            profile, created = Profile.objects.get_or_create(
                account = user,
                defaults={
                    "profile_pic": "https://i.imgur.com/lHubf1C.jpeg",
                }
            )
            # Log the user in after creation
            user = authenticate(username=user.username, password=request.data.get('password'))
            if user: login(request, user)

            profile_serializer = ProfileSerializer(profile)

            return Response({
                'message': 'user created and logged in successfully',
                'user': user_serializer.data,
                'profile':profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# login view
class LoginAPIView(APIView):
    def post(self, request):
        print(request)
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)

        #fetch both puser object and profile
            profile = user.profile if hasattr(user, 'profile') else None
        
            profile_data = ProfileSerializer(profile).data
            user_data = UserSerializer(user).data

            return Response({
                'message': 'Login Successful',
                'user': user_data,
                'profile': profile_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
#logout
class LogoutView(LogoutView):
    next_page = '/'