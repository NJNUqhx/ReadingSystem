import datetime
import random

from django.shortcuts import render, redirect, HttpResponse

from reading_system import models
from reading_system.utils.pagination import Pagination


def exercise_list(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["content__contains"] = search_data
    if nid == 1:
        queryset = models.ExerciseV3.objects.filter(**data_dict).order_by("id")
    elif nid == 2:
        queryset = models.ExerciseV3.objects.filter(**data_dict).order_by("grade")
    else:
        queryset = models.ExerciseV3.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
    }
    return render(request, "exercise_list.html", context)



