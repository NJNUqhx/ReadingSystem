# Generated by Django 4.1.1 on 2023-02-05 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reading_system", "0024_alter_exercisev2result_score_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="exercisev3", name="answer",),
    ]