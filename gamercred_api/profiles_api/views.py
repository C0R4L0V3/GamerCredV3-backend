from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import NotFound
from .models import Profile
from .serializers import ProfileSerializer
from django.http import JsonResponse

# Create your views here.
class ProfileView(generics.ListAPIView):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer

    def retrieve(self, pk=None):
        try:
            #get the user profile using the user Id
            profile = Profile.objects.get(user_id=pk)
            profile_data = ProfileSerializer(profile).data

            res_data = {
                'profile': profile_data
            }

            print(res_data)
            return JsonResponse(res_data)
        except Profile.DoesNotExist:
            raise NotFound('Profile not found')


