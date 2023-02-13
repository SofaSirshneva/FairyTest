from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    number=models.CharField(max_length=25, null=True, unique=True)
    date_of_birth=models.DateField(default='1111-11-11')
    city=models.CharField(max_length=50, default='0')
    country=models.CharField(default='0', max_length=255)
    test_result=models.ManyToManyField('Tests', through="Test_results")
    time_update=models.DateTimeField(auto_now=True)
    mailing=models.BooleanField(default=True)
    avatar=models.ImageField(upload_to='photos/%Y-%m-%d/', default='avatar.png')

class Answers(models.Model):
    text_content = models.TextField(null=True)
    image_content=models.ImageField(upload_to="photos/%Y/%m/%d/", null=True)
    correctness = models.BooleanField(default=False)

class Questions(models.Model):
    text = models.TextField()
    answers = models.ForeignKey('Answers', on_delete=models.PROTECT)

class Tests(models.Model):
    name = models.CharField(max_length=255)
    questions=models.ForeignKey('Questions', on_delete=models.PROTECT)
    rating=models.FloatField(default=0)
    average_result=models.FloatField(default=0)
    number_of_passes=models.IntegerField(default=0)
    time_control=models.IntegerField(null=True)
    author=models.ForeignKey('CustomUser', on_delete=models.PROTECT)
    categorys=models.ManyToManyField('Categories')
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)

class Categories(models.Model):
    name=models.CharField(max_length=255, unique=True)

class Test_results(models.Model):
    test=models.ForeignKey('Tests', on_delete=models.PROTECT)
    user=models.ForeignKey('CustomUser', on_delete=models.PROTECT)
    result=models.FloatField()

