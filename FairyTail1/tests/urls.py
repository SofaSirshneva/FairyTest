from django.urls import path, include
from . import views

urlpatterns = [
    path('createtest', views.TestCreatePage.as_view(), name='createtest'),
    path('addquestion/<slug:test_slug>/<int:que_num>', views.add_question , name='addquestion'),
    path('updatequestion/<slug:tslug>/<int:max>/<int:qnum>', views.update_question, name='updatequestion'),
    path('profile', views.ProfilePage.as_view(), name='profile')
]