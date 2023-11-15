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

from reading_system.views import stu, tec, exercise, account, function, search

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', account.stu_login),
    path('stu/login/', account.stu_login),
    path('stu/logout/', account.stu_logout),
    path('stu/home/', stu.stu_home),
    path('stu/testOne/', stu.stu_testOne),
    path('stu/testOneResult/', stu.stu_testOneResult),
    path('stu/testTwo/', stu.stu_testTwo),
    path('stu/testTwoResult/', stu.stu_testTwoResult),
    path('stu/testThree/', stu.stu_testThree),
    path('stu/testThreeResult/', stu.stu_testThreeResult),
    path('stu/testOneIntroduction/', stu.stu_testOneIntroduction),
    path('stu/testTwoIntroduction/', stu.stu_testTwoIntroduction),
    path('stu/testThreeIntroduction/', stu.stu_testThreeIntroduction),

    path('stu/turnToResult/', stu.stu_turnToResult),
    path('stu/ranklist/', stu.stu_ranklist),
    path('stu/ranklist/<int:test>/', stu.stu_ranklist),
    path('stu/turnpage/', stu.stu_turnpage),

    path('tec/login/', account.tec_login),
    path('tec/logout/', account.tec_logout),
    path('tec/stulist/', tec.tec_stulist),
    path('tec/stuadd/', tec.tec_stuadd),
    path('tec/<int:nid>/stuedit/', tec.tec_stuedit),
    path('tec/<int:nid>/studelete/', tec.tec_studelete),

    path('tec/testlist/', tec.tec_testlist),
    path('tec/<int:nid>/testlist/', tec.tec_testlist),

    path('exercise/list/', exercise.exercise_list),
    path('character/list/', exercise.character_list),
    path('exercise/<int:nid>/list/', exercise.exercise_list),
    path('character/<int:nid>/list/', exercise.character_list),
    path('phrase/list/', exercise.phrase_list),
    path('phrase/<int:nid>/list/', exercise.phrase_list),

    path('tec/testlist/one/', exercise.exercise_testOneList),
    path('tec/testlist/two/', exercise.exercise_testTwoList),
    path('tec/testlist/three/', exercise.exercise_testThreeList),
    path('tec/testlist/one/<int:nid>/', exercise.exercise_testOneList),
    path('tec/testlist/two/<int:nid>/', exercise.exercise_testTwoList),
    path('tec/testlist/three/<int:nid>/', exercise.exercise_testThreeList),

    # 获取准确性题目
    path('stu/exercise/list/<int:nid>/', stu.get_exercise_list),
    # 准确性测试一识别语句
    path('stu/recognition/<int:nid>/', stu.stu_recognizeSpeech),
    # 上传成绩
    path('stu/uploadInfo/<int:nid>/', stu.stu_uploadInfo),

    path('stu/show/list/<int:nid>/', stu.stu_showList),

    # 识别结果
    path('tec/recognition/list/', exercise.recognition_list),

    path('speech/save/', stu.stu_saveSpeech),

    # 测试函数
    path('excel/upload/', function.upload_excel),

    path('test/upload/', function.test_upload),

    path('download/<int:nid>/', function.download_excel),

    # 模拟测试
    path('test/voice/', function.test_voice),
    path('test/correct/', stu.stu_testCorrect),
    path('test/fluency/', function.test_fluency),

    # 汉字属性检索
    path('search/', search.SearchHome),
    path('search/character/', search.SearchCharacter),
    path('search/component/', search.SearchCharacterByComponent),
    path('search/pyin/', search.SearchCharacterByPyin)

]
