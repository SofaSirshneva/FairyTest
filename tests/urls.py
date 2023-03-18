from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MainPage.as_view(), name='main'),
    path('createtest', views.TestCreatePage.as_view(), name='createtest'),
    path('addquestion/<slug:test_slug>/<int:que_num>', views.add_question , name='addquestion'),
    path('updatequestion/<slug:test_slug>/<int:max>/<int:que_num>', views.update_question, name='updatequestion'),
    path('profile', views.ProfilePage.as_view(), name='profile'),
    path('updatetest/<slug:slug>', views.TestUpdatePage.as_view(), name='updatetest'),
    path('categories', views.CategoriesPage.as_view(), name='categories'),
    path('category/<str:name>', views.CategoryPage.as_view(), name='category'),
    path('testinfo/<str:name>', views.TestInfoPage.as_view(), name='testinfo'),
    path('testpassing/<slug:slug>/<int:number>', views.TestPassPage.as_view(), name='testpassing')
]