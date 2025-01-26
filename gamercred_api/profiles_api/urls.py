from .views import ProfileView
from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.ProfileView.as_view(), name='profile'),
    path('profiles/<int:pk>', views.ProfileDetailView.as_view(), name='profile_detail')
]
