from django.db import models
from django.contrib.auth.models import AbstractUser
from tests.models import Tests, Test_results, Questions, Question_results

class CustomUser(AbstractUser):
    number=models.CharField(max_length=25, null=True, unique=True)
    date_of_birth=models.DateField(default='1111-11-11')
    city=models.CharField(max_length=50, default='0')
    country=models.CharField(default='0', max_length=255)
    test_result=models.ManyToManyField(Tests, through=Test_results)
    question_result = models.ManyToManyField(Questions, through=Question_results)
    time_update=models.DateTimeField(auto_now=True)
    mailing=models.BooleanField(default=True)
    avatar=models.ImageField(upload_to='photos/%Y-%m-%d/', default='avatar.png')

