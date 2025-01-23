from django.shortcuts import render
import requests
from django.http import JsonResponse
import os

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
        'steamids': steam_id,
        }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return JsonResponse(response.json()) # should return the steam api response back to the fron end
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)



# a get request by Steam vanity url