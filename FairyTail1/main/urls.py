from django.urls import path, include
from . import views
from main.views import logoutUser, activate 

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('registration', views.Registration.as_view(), name='registration'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', logoutUser, name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'), 
    path('success', views.SuccessPage.as_view(), name='success'),
    path('createtest', views.CreateTestPage.as_view(), name='createtest'),
    path('addquestion/<slug:test_slug>/<int:num_que>', views.AddQuestionPage.as_view(), name = 'addquestion')
]