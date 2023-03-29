# Generated by Django 4.1.5 on 2023-03-04 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='question_result',
            field=models.ManyToManyField(through='tests.Question_results', to='tests.questions'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='test_result',
            field=models.ManyToManyField(through='tests.Test_results', to='tests.tests'),
        ),
    ]