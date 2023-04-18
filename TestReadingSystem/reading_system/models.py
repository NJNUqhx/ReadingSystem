from django.utils import timezone
from django.db import models
from datetime import datetime


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


class Exercise(models.Model):
    content = models.CharField(verbose_name="题目内容", max_length=32, primary_key=True)
    answer = models.BooleanField(verbose_name="正误", default=True)
    total = models.IntegerField(verbose_name="出现总次数", default=0)
    right = models.IntegerField(verbose_name="正确次数", default=0)
    accuracy = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)


class Phrase(models.Model):
    content = models.CharField(verbose_name="题目内容", max_length=8, primary_key=True)
    total = models.IntegerField(verbose_name="出现总次数", default=0)
    right = models.IntegerField(verbose_name="正确次数", default=0)
    accuracy = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)


class ExerciseOfGrade(models.Model):
    content = models.CharField(verbose_name="题目内容", max_length=32)
    grade = models.IntegerField(verbose_name="年级")
    total = models.IntegerField(verbose_name="出现总次数", default=0)
    right = models.IntegerField(verbose_name="正确次数", default=0)
    accuracy = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)


class PhraseOfGrade(models.Model):
    content = models.CharField(verbose_name="题目内容", max_length=8)
    grade = models.IntegerField(verbose_name="年级")
    total = models.IntegerField(verbose_name="出现总次数", default=0)
    right = models.IntegerField(verbose_name="正确次数", default=0)
    accuracy = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)


class ExerciseV1Result(models.Model):
    stu_account = models.CharField(verbose_name="账号", max_length=32)
    name = models.CharField(verbose_name="姓名", max_length=8, default="测试用户")
    grade_choices = (
        (1, "一年级"),
        (2, "二年级"),
        (3, "三年级"),
        (4, "四年级"),
        (5, "五年级"),
        (6, "六年级"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", null=True, default=1, choices=grade_choices)
    total_characters = models.IntegerField(verbose_name="总字数")
    score = models.IntegerField(verbose_name="分数")
    literacy = models.DecimalField(verbose_name="识字量", default=0, decimal_places=2, max_digits=10)
    # 排名实时计算
    accuracy_rate = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)
    exercise_time = models.DateTimeField(verbose_name="时间", default=timezone.now, null=False)
    wrong = models.CharField(verbose_name="错误汉字", default="无", max_length=128)


class ExerciseV2Result(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=8, default="测试用户")
    grade_choices = (
        (1, "一年级"),
        (2, "二年级"),
        (3, "三年级"),
        (4, "四年级"),
        (5, "五年级"),
        (6, "六年级"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", null=True, default=1, choices=grade_choices)
    stu_account = models.CharField(verbose_name="账号", max_length=32, default="njnustu")
    total_characters = models.IntegerField(verbose_name="总字数", default=0)
    wrong_characters = models.IntegerField(verbose_name="错误数", default=0)
    score = models.DecimalField(verbose_name="分数", default=0, decimal_places=2, max_digits=10)
    test_time = models.IntegerField(verbose_name="测试用时", default=0)
    # 排名实时计算
    accuracy_rate = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)
    avg_speed = models.DecimalField(verbose_name="平均阅读速度", default=0, decimal_places=2, max_digits=10)
    exercise_time = models.DateTimeField(verbose_name="时间", default=timezone.now, null=False)
    wrong = models.CharField(verbose_name="错误汉字", default="无", max_length=128)


class ExerciseV3Result(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=8, default="测试用户")
    grade_choices = (
        (1, "一年级"),
        (2, "二年级"),
        (3, "三年级"),
        (4, "四年级"),
        (5, "五年级"),
        (6, "六年级"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", null=True, default=1, choices=grade_choices)
    stu_account = models.CharField(verbose_name="账号", max_length=32, default="njnustu")
    score = models.DecimalField(verbose_name="分数", default=0, decimal_places=2, max_digits=10)
    total_characters = models.IntegerField(verbose_name="总字数", default=0)
    wrong_characters = models.IntegerField(verbose_name="错误数", default=0)
    # 排名实时计算
    accuracy_rate = models.DecimalField(verbose_name="正确率", default=0, decimal_places=2, max_digits=3)
    avg_speed = models.DecimalField(verbose_name="平均阅读速度", default=0, decimal_places=2, max_digits=10)
    exercise_time = models.DateTimeField(verbose_name="时间", default=timezone.now, null=False)
    wrong = models.CharField(verbose_name="错误汉字", default="无", max_length=128)
    judge_all = models.IntegerField(verbose_name="测试句子个数", default=0)
    judge_right = models.IntegerField(verbose_name="判断正确句子个数", default=0)
    judge_accuracy = models.DecimalField(verbose_name="判断正确率", default=0, decimal_places=2, max_digits=3)
    test_time = models.IntegerField(verbose_name="测试用时", default=0)


class Character(models.Model):
    character = models.CharField(verbose_name="汉字", max_length=1, primary_key=True)
    total_time = models.IntegerField(verbose_name="总次数")
    accurate_time = models.IntegerField(verbose_name="正确次数")
    accuracy = models.DecimalField(verbose_name="正确率", decimal_places=2, max_digits=3)


class CharacterOfGrade(models.Model):
    character = models.CharField(verbose_name="汉字", max_length=1)
    grade = models.IntegerField(verbose_name="年级")
    total_time = models.IntegerField(verbose_name="总次数")
    accurate_time = models.IntegerField(verbose_name="正确次数")
    accuracy = models.DecimalField(verbose_name="正确率", decimal_places=2, max_digits=3)


class WavRecognitionResult(models.Model):
    stu = models.CharField(verbose_name="测试学生", max_length=4)
    path = models.CharField(verbose_name="音频路径", max_length=64)
    target = models.CharField(verbose_name="识别目标", max_length=32)
    result = models.CharField(verbose_name="识别结果", max_length=32)
    exercise_time = models.DateTimeField(verbose_name="时间", default=timezone.now, null=False)
