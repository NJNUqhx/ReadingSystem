import datetime
import random

from django.shortcuts import render, redirect, HttpResponse

from reading_system import models
from reading_system.utils.pagination import Pagination


def exercise_list(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    grade = request.GET.get('grade', 0)
    if search_data:
        data_dict["content__contains"] = search_data

    queryset = models.Exercise.objects.filter(**data_dict)

    if nid == 1:
        queryset = models.Exercise.objects.filter(**data_dict).order_by("accuracy")
    elif nid == 2:
        queryset = models.Exercise.objects.filter(**data_dict).order_by("-accuracy")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
        "grade": grade
    }
    return render(request, "exercise_list.html", context)


# 词语题库处理
def phrase_list(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    grade = request.GET.get('grade', 0)
    if search_data:
        data_dict["content__contains"] = search_data

    queryset = models.Phrase.objects.filter(**data_dict)

    if nid == 1:
        queryset = models.Phrase.objects.filter(**data_dict).order_by("accuracy")
    elif nid == 2:
        queryset = models.Phrase.objects.filter(**data_dict).order_by("-accuracy")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
        "grade": grade
    }
    return render(request, "phrase_list.html", context)


def character_list(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    grade = request.GET.get('grade', 0)
    if search_data:
        data_dict["character__contains"] = search_data

    queryset = models.Character.objects.filter(**data_dict)

    if nid == 1:
        queryset = models.Character.objects.filter(**data_dict).order_by("accuracy")
    elif nid == 2:
        queryset = models.Character.objects.filter(**data_dict).order_by("-accuracy")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
        "grade": grade
    }
    return render(request, "character_list.html", context)


def exercise_testOneList(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.ExerciseV1Result.objects.filter(**data_dict)

    if nid == 1:
        queryset = models.ExerciseV1Result.objects.filter(**data_dict).order_by("-score")
    elif nid == 2:
        queryset = models.ExerciseV1Result.objects.filter(**data_dict).order_by("-exercise_time")
    elif nid == 3:
        queryset = models.ExerciseV1Result.objects.filter(**data_dict).order_by("-accuracy_rate")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
    }
    return render(request, "exercise_listOne.html", context)


def exercise_testTwoList(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.ExerciseV2Result.objects.filter(**data_dict)

    if nid == 1:
        queryset = models.ExerciseV2Result.objects.filter(**data_dict).order_by("-score")
    elif nid == 2:
        queryset = models.ExerciseV2Result.objects.filter(**data_dict).order_by("-exercise_time")
    elif nid == 3:
        queryset = models.ExerciseV2Result.objects.filter(**data_dict).order_by("-accuracy_rate")
    elif nid == 4:
        queryset = models.ExerciseV2Result.objects.filter(**data_dict).order_by("-avg_speed")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
    }
    return render(request, "exercise_listTwo.html", context)


def exercise_testThreeList(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.ExerciseV3Result.objects.filter(**data_dict)

    if nid == 1:
        queryset = models.ExerciseV3Result.objects.filter(**data_dict).order_by("-score")
    elif nid == 2:
        queryset = models.ExerciseV3Result.objects.filter(**data_dict).order_by("-exercise_time")
    elif nid == 3:
        queryset = models.ExerciseV3Result.objects.filter(**data_dict).order_by("-judge_accuracy")
    elif nid == 4:
        queryset = models.ExerciseV3Result.objects.filter(**data_dict).order_by("-accuracy_rate")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
    }
    return render(request, "exercise_listThree.html", context)


def exercise_testFourList(request):
    queryset = models.ExerciseV4Result.objects.order_by("-exercise_time")
    page_object = Pagination(request, queryset)
    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "page_string": page_string,
    }
    return render(request, "exercise_listFour.html", context)


def recognition_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["target__contains"] = search_data

    queryset = models.WavRecognitionResult.objects.filter(**data_dict).order_by("-exercise_time")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
    }
    return render(request, "recognition_list.html", context)
