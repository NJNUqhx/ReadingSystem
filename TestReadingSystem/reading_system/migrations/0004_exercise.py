# Generated by Django 4.1.1 on 2022-10-20 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reading_system", "0003_tecinfo_alter_stutestinfo_stu_account_and_more"),
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
                (
                    "test_type",
                    models.SmallIntegerField(
                        choices=[
                            (1, "一年级"),
                            (2, "二年级"),
                            (3, "三年级"),
                            (4, "四年级"),
                            (5, "五年级"),
                            (6, "六年级"),
                        ],
                        default=1,
                        verbose_name="年级",
                    ),
                ),
                ("total_time", models.BigIntegerField(default=0, verbose_name="出现次数")),
                ("wrong_time", models.BigIntegerField(default=0, verbose_name="出错次数")),
                ("content", models.CharField(max_length=32, verbose_name="题目内容")),
                (
                    "answer",
                    models.SmallIntegerField(
                        choices=[(1, "正确"), (2, "错误")], default=1, verbose_name="正误"
                    ),
                ),
            ],
        ),
    ]
