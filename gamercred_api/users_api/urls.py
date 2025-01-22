from django.urls import path
from .views import RegisterUserAPIView, LoginAPIView, LogoutView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]