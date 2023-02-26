from django.db import models

class Answers(models.Model):
    text_content = models.TextField()
    correctness = models.BooleanField(default=False)
    question = models.ForeignKey('Questions', on_delete=models.PROTECT)

class Questions(models.Model):
    text = models.TextField()
    number = models.IntegerField()
    type = models.IntegerField(default=1)
    test = models.ForeignKey('Tests', on_delete=models.PROTECT)

class Tests(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    private=models.BooleanField(default=False)
    password = models.CharField(null=True, max_length=20)
    rating=models.FloatField(default=0)
    average_result=models.FloatField(default=0)
    number_of_passes=models.IntegerField(default=0)
    time_control=models.IntegerField()
    author=models.ForeignKey('main.CustomUser', on_delete=models.PROTECT)
    categories=models.ManyToManyField('Categories')
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)

class Categories(models.Model):
    name=models.CharField(max_length=255, unique=True)

class Test_results(models.Model):
    test=models.ForeignKey('Tests', on_delete=models.PROTECT)
    user=models.ForeignKey('main.CustomUser', on_delete=models.PROTECT)
    result=models.FloatField()

class Question_results(models.Model):
    question=models.ForeignKey('Questions', on_delete=models.PROTECT)
    user=models.ForeignKey('main.CustomUser', on_delete=models.PROTECT)
    answer=models.CharField(null=True, max_length=255)
