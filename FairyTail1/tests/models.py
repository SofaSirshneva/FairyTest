from django.db import models

class Answers(models.Model):
    text_content = models.TextField(null=True)
    image_content=models.ImageField(upload_to="photos/%Y/%m/%d/", null=True)
    correctness = models.BooleanField(default=False)
    question = models.ForeignKey('Questions', on_delete=models.PROTECT, default='', null=True)

class Questions(models.Model):
    text = models.TextField()
    number = models.IntegerField(null=True)
    test = models.ForeignKey('Tests', on_delete=models.PROTECT, default='', null=True)

class Tests(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", default='')
    private=models.BooleanField(default=False)
    password = models.CharField(null=True, max_length=20)
    rating=models.FloatField(default=0)
    average_result=models.FloatField(default=0)
    number_of_passes=models.IntegerField(default=0)
    time_control=models.IntegerField(null=True)
    author=models.ForeignKey('main.CustomUser', on_delete=models.PROTECT)
    categories=models.ManyToManyField('Categories', default='')
    time_create=models.DateTimeField(auto_now_add=True)
    time_update=models.DateTimeField(auto_now=True)

class Categories(models.Model):
    name=models.CharField(max_length=255, unique=True)

class Test_results(models.Model):
    test=models.ForeignKey('Tests', on_delete=models.PROTECT)
    user=models.ForeignKey('main.CustomUser', on_delete=models.PROTECT)
    result=models.FloatField()
