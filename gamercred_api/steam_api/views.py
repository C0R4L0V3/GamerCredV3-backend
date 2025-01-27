import openid
import os
import requests
from django.conf import settings
from urllib.parse import urlencode
from openid.consumer.consumer import Consumer, SUCCESS
from openid.store.filestore import FileOpenIDStore
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import View

from rest_framework.views import APIView
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

# a get request to get the steam ID
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
    

# a get request get the Steam vanity url
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
    

#fetch a list of recently played games by player steam ID
def get_game_list(request):
    #need to pass the found players steam id as param
    steam_id = request.GET.get('steamid')

    if not steam_id:
        return JsonResponse({'error': 'Steam Id required'}, status=400)
    
    #this would fetch most recently played games
    url = f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/'
    params = {
        'key': STEAM_KEY,
        'steamid': steam_id,
        'include_appinfo': True, # this should include game names and other info
        'include_played_free_games': True # should include free to play games
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()

        data = res.json()
        # print(data)
        games = data.get('response', {}).get('games', [])
        # print(games)
        if not games:
            return JsonResponse({'message': 'No games found for this Player.'}, status=200)
        
        return JsonResponse({'recent_games': games}, status=200)

        # game_list = [{'appid': game['appid'], 'name': game['name'], 'playtime': game['playtime_forever'], 'img_icon_url': game['img_icon_url']} for game in games]
        # return JsonResponse({'games': game_list}, status=200)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500 )
    
#Get complete list of all games owned by player ID
def get_complete_game_list(request):
    #need to pass the found players steam id as param
    steam_id = request.GET.get('steamid')

    if not steam_id:
        return JsonResponse({'error': 'Steam Id required'}, status=400)

    #this would fetch all the players owned games
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': STEAM_KEY,
        'steamid': steam_id,
        'include_appinfo': True, # this should include game names and other info
        'include_played_free_games': True # should include free to play games
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()

        data = res.json()
        # print(data)
        games = data.get('response', {}).get('games', [])
        # print(games)
        if not games:
            return JsonResponse({'message': 'No games found for this Player.'}, status=200)
        
        return JsonResponse({'all_games': games}, status=200)

        # game_list = [{'appid': game['appid'], 'name': game['name'], 'playtime': game['playtime_forever'], 'img_icon_url': game['img_icon_url']} for game in games]
        # return JsonResponse({'games': game_list}, status=200)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500 )
    

    

    #This would the player's achievemtns for a specific game, will likely not incorperate
def get_player_achievements(request):

    # This would be game specific

    app_id = request.GET.get('appid')

    if not app_id:
        return JsonResponse({'error': 'Steam Id required'}, status=400)
    
    url = f'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/'
    params = {
        'key': STEAM_KEY,
        'appid': app_id,
        #maybe there are other option things i can include???
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()

        data = res.json()
        print(data)
        #this may or may not exsist?
        # achievments = data.get('response', {}).get('achievement', [])

        if not data:
            return JsonResponse({'message': 'no achievements found for this player.'}, status=200)
        
        return JsonResponse({'response': res.json()}, status=200)
    
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    



#link steam account to user profile
    #steam login
@method_decorator(login_required, name='dispatch')
class SteamLoginView(LoginView):
    def get(self, request):

        if not request.user.is_authenticated:
            return JsonResponse({'message': 'user must be logged in'}, status=401)
        
        # need to pass the target user's id in the return_to url
        user_id = request.GET.get('user_id')

        print('user id: ', user_id )
        return_to_url = f'http://localhost:8000/link-steam/callback/?user_id={user_id}'
        gamercred_steam_openid = SteamOpenID(
            realm="http://localhost:8000/link-steam/",
            return_to=return_to_url
        )

        try:
            redirect_url = gamercred_steam_openid.get_redirect_url()
            return HttpResponseRedirect(redirect_url)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



    #callback view
@method_decorator(login_required, name='dispatch')
class SteamCallbackView(View):
    def get(self, request):

        try:
            #retrive the user Id from the return_to query
            user_id = request.GET.get('user_id')
            print('user id: ', user_id)

            if not user_id:
                return JsonResponse({'error': 'user id not provided'}, status=400)
            try:
                user = User.objects.get(id=user_id)
                print('user: ', user)
            except User.DoesNotExist:
                return JsonResponse({'error': 'user not found'}, status=404)

            #verifies that the user has a profile
            try:
                profile = Profile.objects.get(account=user)
                print("profile found: ", profile)
            except Profile.DoesNotExist:
                return JsonResponse({'error': 'User has no profile'}, status=400)
            
            #process the openid response
            openid_store = FileOpenIDStore(str(settings.BASE_DIR) + '/openid_store')
            consumer = Consumer(session={}, store=openid_store)
            response = consumer.complete(dict(request.GET.items()), request.build_absolute_uri())

            if response.status != SUCCESS:
                return JsonResponse({'message': 'Steam authentication failed'}, status=400)
            
            
            #extract the and save steam ID
            openid_url = response.getDisplayIdentifier()
            steam_id = openid_url.split('/')[-1]

            print('Steam Id: ', steam_id)

            profile.steam_id = steam_id 
            profile.save()

            return JsonResponse({'message': 'Steam account linked successfully', 'steam_id': steam_id}, status=200)

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

        # steam_id = gamercred_steam_openid.validate_results(request.query_params)
                   # steam_id = gamercred_steam_openid.process(request.GET)
            # if steam_id:

                  # #so the issue is it is the admin that is trying to make the request to link the account not the user that is registering.
            # print("Request user: ", request.user)
            # print("Authenticated: ", request.user.is_authenticated)

                          # Simulate a successful login (e.g., creating or finding a user)
                # Optionally, generate a token here for frontend use (JWT example)


            # if not request.user.is_authenticated:
                # return JsonResponse({'message': 'user must be logged in'}, status=401)
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
                        #redirects the front end back to the home page ( have it redirect back to another page later on)
            # return HttpResponseRedirect(f"http://localhost:8000/")
            # else:
            #     return JsonResponse({'error': 'Failed to Authenticate'}, status=403)
