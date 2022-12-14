# Generated by Django 4.1.1 on 2022-10-10 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "reading_system",
            "0002_remove_stutestinfo_test_time_stutestinfo_score_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="TecInfo",
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
                    "tec_account",
                    models.CharField(default="tec", max_length=32, verbose_name="账号"),
                ),
                (
                    "tec_password",
                    models.CharField(
                        default="njnutec", max_length=32, verbose_name="密码"
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="stutestinfo",
            name="stu_account",
            field=models.CharField(default="njnustu", max_length=32, verbose_name="账号"),
        ),
        migrations.AlterField(
            model_name="stutestinfo",
            name="stu_name",
            field=models.CharField(default="stu", max_length=32, verbose_name="学生"),
        ),
        migrations.AddField(
            model_name="stuexactinfo",
            name="admintec",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="reading_system.tecinfo",
                verbose_name="管理员",
            ),
        ),
    ]
