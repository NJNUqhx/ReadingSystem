# Generated by Django 4.1.1 on 2023-02-07 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reading_system", "0029_exercisev3result_judge_accuracy_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="exercisev3result",
            name="test_time",
            field=models.IntegerField(default=0, verbose_name="测试用时"),
        ),
        migrations.AlterField(
            model_name="exercisev2result",
            name="test_time",
            field=models.IntegerField(default=0, verbose_name="测试用时"),
        ),
    ]
