# Generated by Django 4.1.5 on 2023-02-26 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_alter_question_results_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_results',
            name='answer',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
