from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('enter', views.EnterPage.as_view(), name='enter')
]