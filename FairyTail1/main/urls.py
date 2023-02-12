from django.urls import path, include
from . import views
from main.views import logoutUser

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', logoutUser, name='logout')
]