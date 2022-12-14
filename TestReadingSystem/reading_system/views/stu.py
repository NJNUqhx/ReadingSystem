import datetime
import json
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from reading_system import models
from reading_system.utils.pagination import Pagination
from reading_system.utils.chooseList import gen

def stu_home(request):
    print(gen.getChart())
    return render(request, "stu_home.html")


def stu_show(request, nid=0):
    # 按照名字搜索相应记录
    dic = request.session.get('info')
    name = dic['name']
    if nid == 1:
        queryset = models.StuTestInfo.objects.filter(stu_name=name).order_by("score")
        queryset.reverse()
    elif nid == 2:
        queryset = models.StuTestInfo.objects.filter(stu_name=name).order_by("test_type")
    else:
        queryset = models.StuTestInfo.objects.filter(stu_name=name).order_by("id")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "page_string": page_string,
    }
    return render(request, "stu_show.html", context)


def stu_testOne(request):
    return render(request, "stu_testOne.html")


@csrf_exempt
def stu_testOneResult(request):

    context = {
        "speed": "每分钟阅读正确5个汉字",
        "rank": "24/180",
    }
    return render(request, "stu_testOneResult.html", context)


def stu_testTwoResult(request):
    context = {
        "speed": "每分钟阅读正确5个汉字",
        "rank": "24/180",
    }
    return render(request, "stu_testOneResult.html", context)


def stu_testThreeResult(request):
    context = {
        "content": "读错的汉字或句子",
        "speed": "每分钟阅读正确5个汉字",
        "rank": "24/180",
        "tips": "阅读建议",
        "extra": "其他信息"
    }
    return render(request, "stu_testOneResult.html", context)

# 获取对应年级的题目
def get_exercise_list(grade=1):
    exercise_list = models.ExerciseV3.objects.filter(grade=grade)
    return exercise_list


def stu_testThree(request):
    exerciseList = get_exercise_list()
    exercise = exerciseList[0]
    return render(request, "stu_testThree.html", {"exercise": exercise})
    # return render(request, "stu_testThree.html", {
    #     'List': json.dumps(exerciseList),
    # })


def stu_testOneIntroduction(request):
    request.session['type'] = 1
    return render(request, "testOneIntroduction.html")


def stu_testTwoIntroduction(request):
    request.session['type'] = 2
    return render(request, "testTwoIntroduction.html")


def stu_testThreeIntroduction(request):
    print("I am here")
    request.session['type'] = 3
    return render(request, "testThreeIntroduction.html")


@csrf_exempt
def stu_uploadInfo(request):
    dic = request.session.get('info')
    if request.method == "POST":
        exercise = get_exercise_list()[2].content
        test_dict = request.POST
        # if dic['type'] == 3:
        #     result = models.ExerciseV3.objects.filter(content=test_dict['content'])
        #     print(result)
        return JsonResponse({"status": True, "exercise": exercise})

def stu_uploadInfoOfTestThree(request):
    dic = request.session.get('info')
    if request.method == "POST":
        exercise = get_exercise_list()[2].content
        test_dict = request.POST
        return JsonResponse({"status": True, "exercise": exercise})

@csrf_exempt
def stu_turnToResult(request):
    if request.method == "POST":
        print(request.POST)
        return JsonResponse({"status": True})


## 排行榜
def stu_ranklist(request, test=1):
    grade = request.session.get('info')['grade']
    ranklist = models.StuTestInfo.objects.filter(grade=grade).filter(test_type=test).order_by("score").reverse()
    grade_arr = ["未知", "一年级", "二年级", "三年级", "四年级", "五年级", "六年级"]
    test_arr = ["未知", "阅读准确性测试", "阅读流畅性测试一", "阅读流畅性测试二"]
    context = {
        "ranklist": ranklist,
        "grade": grade_arr[grade],
        "test": test_arr[test],
    }
    return render(request, "stu_ranklist.html", context)


## 跳转界面
def stu_turnpage(request):
    dic = request.session.get('info')
    status = dic["exercise"]
    next_exercise = [0, 1, 2]
    tar_html = [
        "testOneIntroduction.html",
        "testTwoIntroduction.html",
        "testThreeIntroduction.html",
    ]
    random.shuffle(next_exercise)
    if not status[next_exercise[0]]:
        request.session['info']['exercise'][0] = True
        return render(request, tar_html[next_exercise[0]])
    elif not status[next_exercise[1]]:
        request.session['info']['exercise'][1] = True
        return render(request, tar_html[next_exercise[1]])
    elif not status[next_exercise[2]]:
        request.session['info']['exercise'][2] = True
        return render(request, tar_html[next_exercise[2]])
    request.session['info']['exercise'][0] = False
    request.session['info']['exercise'][1] = False
    request.session['info']['exercise'][2] = False
    return HttpResponse("跳转页面")
