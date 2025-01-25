import openid
import os
import requests
from django.conf import settings
from urllib.parse import urlencode
from openid.consumer.consumer import Consumer, SUCCESS
from openid.store.filestore import FileOpenIDStore
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from profiles_api.models import Profile

# from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from steam_openid import SteamOpenID
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


gamercred_steam_openid = SteamOpenID(
    realm="http://localhost:8000/link-steam/",
    return_to="http://localhost:8000/link-steam/callback/",
)


STEAM_KEY = os.getenv('STEAM_API_KEY')

# Create your views here.

# a get request by steam ID
def get_steam_user(request):
    steam_id = request.GET.get('steamid')
    if not steam_id:
        return JsonResponse({'error': 'Steam Id is required'}, status=400)

    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    params = {
        'key': STEAM_KEY,
        # this is to target the steamIds field parameter
        'steamids': steam_id,
        }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return JsonResponse(res.json()) # should return the steam api response back to the fron end
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

# a get request by Steam vanity url
def get_steam_vanity(request):
    vanity = request.GET.get('vanityurl')
    if not vanity:
        return JsonResponse({'error': 'Steam Vanity is required'}, status=400)

    url = f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
    params = {
        'key': STEAM_KEY,
        'vanityurl': vanity,
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return JsonResponse(res.json())
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

#link steam account to user profile
    #steam login
class SteamLoginView(LoginView):
    def get(self, request):
        # this should redirect the user to Steam's openId login page
        # steam_openid_url = 'https://steamcommunity.com/openid/login'
        #
        # params = {
        #     'openid.ns': 'http://specs.openid.net/auth/2.0',
        #     'openid.mode': 'checkedid_setup',
        #     'openid.return_to': settings.SITE_URL + '/link-steam/callback/',
        #     'openid.realm': settings.SITE_URL,
        #     'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        #     'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
        # }
        #
        #
        # #generate the full OpenId URL
        # redirect_url = f"{steam_openid_url}?{urlencode(params)}"
        # return JsonResponse({ "redirect_url" : redirect_url })

        try:
            redirect_url = gamercred_steam_openid.get_redirect_url()
            return HttpResponseRedirect(redirect_url)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    #callback view
class SteamCallbackView(View):
    def get(self, request):
        #extract the openid info from the request
        # openid_url = request.GET.get('openid.identity')
        #extract the steam Id from the open id url
        # openid_response = dict(request.GET.item())
        # openid_store = FileOpenIDStore(settings.BASE_DIR / '/openid_store')
        # consumer = Consumer({}, openid_store)
        #
        # response = consumer.complete(dict(request.GET), request.build_absolute_uri())
        #
        # if response.status != SUCCESS:
        #     return JsonResponse({'message': 'Steam authentication failed'}, status=400)
        #
        # openid_url = response.getDisplayIdentifier()
        # steam_id = openid_url.split('/')[-1]
        #
        # if not steam_id:
        #     return JsonResponse({'message': "Steam Id not found"}, status=400)
        #
        # if not request.user.is_authenticated:
        #     return JsonResponse({'message': 'user must be logged in'}, status=401)
        #
        # profile = request.user.profile
        # profile.steam_id = steam_id
        # profile.save()
        #
        # return JsonResponse({'message': 'steam account linked successfully', 'steam_id': steam_id}, status=200)

        steam_id = gamercred_steam_openid.validate_results(request.query_params)
        try:
            steam_id = gamercred_steam_openid.process(request.GET)
            if steam_id:
                # Simulate a successful login (e.g., creating or finding a user)
                # Optionally, generate a token here for frontend use (JWT example)
                        profile = request.user.profile
                        profile.steam_id = steam_id
                        profile.save()
                return JsonResponse({'success': True, 'steam_id': steam_id})
            else:
                return JsonResponse({'error': 'Failed to Authenticate'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# class LinkSteamAccountAPIView(APIView):
#     def post(self, request):
#         steam_id = request.data.get('steamId')

#         if not steam_id:
#             return Response({"message": "Steam"})

    #     return super().get(request) # should redirect to steam openId page

    # def post(self, request):
    #     openid_url = request.POST.get('openid_url')
    #     #should handl openid verification from steam
    #     return redirect("steam_success")

    # def steam_success(request):
    #     #process the response and link the steam id to the user profil
    #     steam_id = request.user.profile.steam_id
    #     return redirect('profile')
