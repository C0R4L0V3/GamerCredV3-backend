from django.urls import path
from . import views
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.socialaccount.providers.steam import provider

urlpatterns = [
    # default_urlpatterns(provider.Provider),
    path('api/steam_user/', views.get_steam_user, name='get_steam_user'),
    path('api/steam_vanity/', views.get_steam_vanity, name="get_steam_vanity"),
    path('link-steam/', views.SteamLoginView.as_view(), name='steam_login'), # this hould start the login for steam
    path('link-steam/callback/', views.SteamCallbackView.as_view(), name='steam_callback'), # callback to handle steams response
    path('game-list/', views.get_game_list, name='get_game_list'),
    path('player-achievements/', views.get_player_achievements, name='get_player_achievements'),
    path('complete-game-list/', views.get_complete_game_list, name='get_complete_game_list')
]

'''
path('api/steam_user/', views.get_steam_user, name='get_steam_user'),
path('api/steam_vanity/', views.get_steam_vanity, name="get_steam_vanity"),
path('link-steam/', SteamLoginView.as_view(), name='steam_login'), # this hould start the login for steam
path('link-steam/callback/', SteamCallbackView.as_view(), name='steam_callback'), # callback to handle steams response
'''