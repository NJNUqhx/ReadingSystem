from django.utils import timezone
from django.db import models
from datetime import datetime

# Create your models here.
'''
普通用户
    个人详细信息表格
    (1) name
    (2) age
    (3) regisiter_time
    (4) account (id + 1000000)
    (5) password
    
    测试信息表格
    (1) account
    (2) type
    (3) score
'''


class StuExactInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    grade_choices = (
        (1, "一年级"),
        (2, "二年级"),
        (3, "三年级"),
        (4, "四年级"),
        (5, "五年级"),
        (6, "六年级"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", null=True, default=1, choices=grade_choices)
    account = models.CharField(verbose_name="账号", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)

    admintec = models.ForeignKey(verbose_name="管理员", null=True, to="TecInfo", to_field="id",
                                 on_delete=models.CASCADE)


class StuTestInfo(models.Model):
    stu_name = models.CharField(verbose_name="学生", max_length=32, default="stu")
    stu_account = models.CharField(verbose_name="账号", max_length=32, default="njnustu")
    grade_choices = (
        (1, "一年级"),
        (2, "二年级"),
        (3, "三年级"),
        (4, "四年级"),
        (5, "五年级"),
        (6, "六年级"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", null=True, default=1, choices=grade_choices)
    time = models.DateTimeField(verbose_name="时间", default=timezone.now, null=False)
    type_choices = (
        (1, "准确性测试"),
        (2, "流畅性测试一"),
        (3, "流畅性测试二"),
    )
    test_type = models.SmallIntegerField(verbose_name="类型", choices=type_choices, default=1)
    score = models.DecimalField(verbose_name="分数", decimal_places=2, max_digits=4, default=0)


class TecInfo(models.Model):
    tec_account = models.CharField(verbose_name="账号", max_length=32, default="tec")
    tec_password = models.CharField(verbose_name="密码", max_length=32, default="njnutec")

    def __str__(self):
        return self.tec_account


class ExerciseV3(models.Model):
    grade_choices = (
        (1, "一年级"),
        (2, "二年级"),
        (3, "三年级"),
        (4, "四年级"),
        (5, "五年级"),
        (6, "六年级"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", choices=grade_choices, default=1)
    total_time = models.BigIntegerField(verbose_name="出现次数", default=0)
    wrong_time = models.BigIntegerField(verbose_name="出错次数", default=0)

    content = models.CharField(verbose_name="题目内容", max_length=32)
    answer_choices = (
        (1, "正确"),
        (2, "错误"),
    )
    answer = models.SmallIntegerField(verbose_name="正误", choices=answer_choices, default=1)

class ExerciseV1Result(models.Model):
    stu_account = models.CharField(verbose_name="账号", max_length=32, default="njnustu")
    total_characters = models.IntegerField(verbose_name="总字数", default=0)
    score = models.DecimalField(verbose_name="分数", default=0, decimal_places=2, max_digits=3)
    # 排名实时计算
    accuracy_rate = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)

class ExerciseV2Result(models.Model):
    stu_account = models.CharField(verbose_name="账号", max_length=32, default="njnustu")
    total_characters = models.IntegerField(verbose_name="总字数", default=0)
    wrong_characters = models.IntegerField(verbose_name="错误数", default=0)
    score = models.DecimalField(verbose_name="分数",default=0, decimal_places=2, max_digits=3)
    test_time = models.CharField(verbose_name="测试用时", max_length=100, default=60)
    # 排名实时计算
    accuracy_rate = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)
    avg_speed = models.DecimalField(verbose_name="平均阅读速度", default=0, decimal_places=2, max_digits=3)


class ExerciseV3Result(models.Model):
    stu_account = models.CharField(verbose_name="账号", max_length=32, default="njnustu")
    score = models.DecimalField(verbose_name="分数",default=0,decimal_places=2,max_digits=3)
    total_characters = models.IntegerField(verbose_name="总字数", default=0)
    wrong_characters = models.IntegerField(verbose_name="错误数", default=0)
    # 排名实时计算
    accuracy_rate = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2,max_digits=3)
    avg_speed = models.DecimalField(verbose_name="平均阅读速度", default=0, decimal_places=2,max_digits=3)
