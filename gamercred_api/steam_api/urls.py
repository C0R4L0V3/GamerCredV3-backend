from django.urls import path
from . import views

urlpatterns = [
    path('api/steam_user', views.get_steam_user, name='get_steam_user'),
]