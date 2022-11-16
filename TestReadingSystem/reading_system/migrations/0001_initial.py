# Generated by Django 4.1.1 on 2022-10-09 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StuExactInfo",
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
                ("name", models.CharField(max_length=32, verbose_name="姓名")),
                ("age", models.IntegerField(verbose_name="年龄")),
                ("account", models.CharField(max_length=32, verbose_name="账号")),
                ("password", models.CharField(max_length=32, verbose_name="密码")),
            ],
        ),
        migrations.CreateModel(
            name="StuTestInfo",
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
                ("test_time", models.DateTimeField(verbose_name="测试时间")),
            ],
        ),
    ]
