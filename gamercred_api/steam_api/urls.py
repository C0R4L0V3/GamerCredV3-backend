from django.urls import path
from . import views

urlpatterns = [
    path('api/steam_user/', views.get_steam_user, name='get_steam_user'),
    path('api/steam_vanity/', views.get_steam_vanity, name="get_steam_vanity"),

]