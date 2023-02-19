from django.urls import path, include
from . import views

urlpatterns = [
    path('createtest', views.TestCreatePage.as_view(), name='createtest'),
    path('addquestion/<slug:que_slug>/<int:max>/<int:que_num>', views.add_question , name='addquestion'),
    path('updatequestion/<slug:qslug>/<int:max>/<int:qnum>', views.update_question, name='updatequestion')
]