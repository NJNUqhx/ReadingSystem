# Generated by Django 4.1.1 on 2023-02-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reading_system", "0026_exercisev3_answer"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=32, verbose_name="题目内容")),
                ("answer", models.BooleanField(default=True, verbose_name="正误")),
            ],
        ),
        migrations.DeleteModel(name="ExerciseV3",),
    ]
