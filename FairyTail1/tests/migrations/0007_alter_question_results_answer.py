# Generated by Django 4.1.5 on 2023-02-26 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0006_rename_test_question_results_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_results',
            name='answer',
            field=models.FloatField(null=True),
        ),
    ]
