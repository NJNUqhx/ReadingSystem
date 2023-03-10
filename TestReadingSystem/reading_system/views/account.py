import json
from django.shortcuts import render, HttpResponse, redirect
from django import forms
from django.core.exceptions import ValidationError

from reading_system import models
from reading_system.utils.pagination import Pagination
from reading_system.utils.bootstrap import BootStrapForm


class TecLoginForm(BootStrapForm):
    tec_account = forms.CharField(label="账号", widget=forms.TextInput, required=True)
    tec_password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)


def tec_login(request):
    if request.method == "GET":
        form = TecLoginForm()
        return render(request, "tec_login.html", {"form": form})

    form = TecLoginForm(data=request.POST)
    if form.is_valid():
        tec_object = models.TecInfo.objects.filter(**form.cleaned_data).first()
        if not tec_object:
            form.add_error("tec_password", "用户名或密码错误")
            return render(request, 'tec_login.html', {'form': form})
        request.session["info"] = {"account": tec_object.tec_account, "password": tec_object.tec_password}
        return redirect("/tec/stulist/")
    return render(request, 'tec_login.html', {'form': form})


def tec_logout(request):
    request.session.clear()
    return redirect("/tec/login/")


class StuLoginForm(BootStrapForm):
    account = forms.CharField(label="账号", widget=forms.TextInput, required=True)
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True), required=True)


def stu_login(request):
    if request.method == "GET":
        form = StuLoginForm()
        return render(request, "stu_login.html", {"form": form})

    form = StuLoginForm(data=request.POST)
    if form.is_valid():
        stu_object = models.StuExactInfo.objects.filter(**form.cleaned_data).first()
        if not stu_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'stu_login.html', {'form': form})
        request.session["info"] = {"account": stu_object.account, "name": stu_object.name, "age": stu_object.age,
                                   "grade": stu_object.grade,
                                   "exercise": [False, False, False], "type": 0}
        return redirect("/stu/home/")
    return render(request, 'stu_login.html', {'form': form})


def stu_logout(request):
    request.session.clear()
    return redirect("/stu/login/")
