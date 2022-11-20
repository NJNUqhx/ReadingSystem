"""TestReadingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from reading_system.views import stu, tec, exercise, account

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('stu/login/', account.stu_login),
    path('stu/logout/', account.stu_logout),
    path('stu/home/', stu.stu_home),
    path('stu/show/', stu.stu_show),
    path('stu/<int:nid>/show/', stu.stu_show),
    path('stu/testOne/', stu.stu_testOne),
    path('stu/testOneResult/', stu.stu_testOneResult),
    path('stu/testThree/', stu.stu_testThree),
    path('stu/testOneIntroduction/', stu.stu_testOneIntroduction),
    path('stu/testTwoIntroduction/', stu.stu_testTwoIntroduction),
    path('stu/testThreeIntroduction/', stu.stu_testThreeIntroduction),
    path('stu/uploadInfo/', stu.stu_uploadInfo),
    path('stu/uploadInfoOfTestThree/', stu.stu_uploadInfoOfTestThree),
    path('stu/turnToResult/', stu.stu_turnToResult),
    path('stu/ranklist/', stu.stu_ranklist),
    path('stu/ranklist/<int:test>/', stu.stu_ranklist),
    path('stu/turnpage/', stu.stu_turnpage),

    path('tec/login/', account.tec_login),
    path('tec/logout', account.tec_logout),
    path('tec/stulist/', tec.tec_stulist),
    path('tec/stuadd/', tec.tec_stuadd),
    path('tec/<int:nid>/stuedit/', tec.tec_stuedit),
    path('tec/<int:nid>/studelete/', tec.tec_studelete),

    path('tec/testlist/', tec.tec_testlist),
    path('tec/<int:nid>/testlist/', tec.tec_testlist),

    path('exercise/list/', exercise.exercise_list),
    path('exercise/<int:nid>/list/', exercise.exercise_list),

]
