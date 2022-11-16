from django.shortcuts import render, redirect, HttpResponse

from reading_system import models
from reading_system.utils.pagination import Pagination
from reading_system.utils.form import StuModelForm, StuEditModelForm


def tec_stulist(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["name__contains"] = search_data

    queryset = models.StuExactInfo.objects.filter(**data_dict).order_by("id")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
    }
    return render(request, "tec_stulist.html", context)


def tec_stuadd(request):
    if request.method == "GET":
        form = StuModelForm()
        return render(request, "tec_stuadd.html", {"form": form})

    form = StuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/tec/stulist/')
    else:
        return render(request, "tec_stuadd.html", {"form": form})


def tec_stuedit(request, nid):
    row_object = models.StuExactInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = StuEditModelForm(instance=row_object)
        return render(request, "tec_stuedit.html", {"form": form})

    form = StuEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/tec/stulist/')
    else:
        return render(request, "tec_stuedit.html", {"form": form})


def tec_studelete(request, nid):
    models.StuExactInfo.objects.filter(id=nid).delete()
    return redirect('/tec/stulist/')


def tec_testlist(request, nid=0):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["stu_name__contains"] = search_data
    if nid == 1:
        queryset = models.StuTestInfo.objects.filter(**data_dict).order_by("score")
    elif nid == 2:
        queryset = models.StuTestInfo.objects.filter(**data_dict).order_by("stu_name")
    elif nid == 3:
        queryset = models.StuTestInfo.objects.filter(**data_dict).order_by("test_type")
    else:
        queryset = models.StuTestInfo.objects.filter(**data_dict).order_by("id")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "search_data": search_data,
        "page_string": page_string,
    }
    return render(request, "tec_testlist.html", context)

