from django.urls import path
from .views import *
from pathlib import PurePath
import os

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='registration'),
    path('register/confirm/', RegistrationConfirm.as_view(), name='confirm'),
    path('verify/<str:username>/<str:key>/',
         VerifyEmail.as_view(), name='verify'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('update/', UserUpdateView.as_view(), name='update'),
]
