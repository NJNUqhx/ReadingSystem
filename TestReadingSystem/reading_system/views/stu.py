import datetime
import json
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from reading_system import models
from reading_system.utils.pagination import Pagination
from reading_system.utils.chooseList import gen
from reading_system.utils.Voice import voice
from reading_system.models import ExerciseV1Result
from reading_system.models import ExerciseV2Result
from reading_system.models import ExerciseV3Result
from reading_system.models import Character
from reading_system.models import WavRecognitionResult
from reading_system.models import CharacterOfGrade
from reading_system.models import ExerciseOfGrade
from reading_system.utils.phrase import phrase
from reading_system.models import Phrase
from reading_system.models import PhraseOfGrade

from reading_system.utils.Voice2 import ifly_recognize
from reading_system.utils import chinesecharacter
from reading_system.utils.chinesecharacter import JudgePyInSentence, IsSimilarChar, CompareChar, LCS, LCS_str, GenExerciseList



def stu_home(request):
    info = request.session.get("info")
    if not info:
        return redirect("/stu/login/")
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

def stu_testTwo(request):
    return render(request, "stu_testTwo.html")

def stu_testCorrect(request):
    return render(request, "test_correct.html")

@csrf_exempt
def stu_testOneResult(request):
    dic = request.session.get('info')
    row_object = models.ExerciseV1Result.objects.filter(stu_account=dic["account"]).last()
    content = row_object.wrong
    greater = models.ExerciseV1Result.objects.filter(score__gt=row_object.score).count()
    all = models.ExerciseV1Result.objects.count()
    rank = str(greater + 1) + "/" + str(all)
    accuracy = row_object.accuracy_rate
    score = row_object.score
    context = {
        "content":content,
        "accuracy": accuracy,
        "rank": rank,
        "score": score,
        "tips": "略"
    }
    return render(request, "stu_testOneResult.html", context)

def stu_testTwoResult(request):
    dic = request.session.get('info')
    row_object = models.ExerciseV2Result.objects.filter(stu_account=dic["account"]).last()
    wrong = row_object.wrong
    greater = models.ExerciseV2Result.objects.filter(score__gt=row_object.score).count()
    all = models.ExerciseV2Result.objects.count()
    rank = str(greater + 1) + "/" + str(all)
    accuracy = row_object.accuracy_rate
    speed = str(row_object.avg_speed)
    score = row_object.score
    context = {
        "wrong": wrong,
        "accuracy": accuracy,
        "rank": rank,
        "speed": "每分钟阅读正确" + speed + "个汉字",
        "score": score,
        "tips": "略"
    }
    return render(request, "stu_testTwoResult.html", context)


def stu_testThreeResult(request):
    dic = request.session.get('info')
    row_object = models.ExerciseV3Result.objects.filter(stu_account=dic["account"]).last()
    wrong = row_object.wrong
    greater = models.ExerciseV3Result.objects.filter(score__gt=row_object.score).count()
    all = models.ExerciseV3Result.objects.count()
    rank = str(greater + 1) + "/" + str(all)
    accuracy = row_object.judge_accuracy
    speed = str(row_object.avg_speed)
    score = row_object.score
    context = {
        "wrong": wrong,
        "speed": "每分钟阅读正确" + speed + "个汉字",
        "rank": rank,
        "score": score,
        "accuracy": accuracy
    }
    return render(request, "stu_testThreeResult.html", context)


# 获取对应年级的题目

# 获取题目
def stu_testThree(request):
    exercise = "exerciseList[0]"
    return render(request, "stu_testThree.html", {"exercise": exercise})



def stu_testOneIntroduction(request):
    request.session['type'] = 1
    return render(request, "testOneIntroduction.html")


def stu_testTwoIntroduction(request):
    request.session['type'] = 2
    return render(request, "testTwoIntroduction.html")


def stu_testThreeIntroduction(request):
    request.session['type'] = 3
    return render(request, "testThreeIntroduction.html")


@csrf_exempt
def stu_uploadInfo(request, nid=0):
    dic = request.session.get('info')
    grade = int(dic["grade"])
    name = dic["name"]
    receive = request.POST
    # print(receive)
    if nid == 0:
        result_v1 = ExerciseV1Result(stu_account=dic["account"],name=name,grade=grade)
        result_v1.literacy = receive["literacy"]
        if 3 <= grade <= 6:
            result_v1.literacy = float(receive["literacy"]) + 295
        result_v1.total_characters = receive["total"]
        result_v1.score = receive["score"]
        if int(receive["total"]) != 0:
            result_v1.accuracy_rate = float(receive["score"]) / float(receive["total"])
        result_v1.wrong = receive["wrong"]
        result_v1.save()
        return JsonResponse({"status": True})
    elif nid == 1:
        result_v2 = ExerciseV2Result(stu_account=dic["account"],name=name,grade=grade)
        result_v2.total_characters = receive["total"]
        result_v2.wrong_characters = int(receive["total"]) - int(receive["right"])
        if int(receive["total"]) != 0:
            result_v2.accuracy_rate = float(receive["right"]) / float(receive["total"])
        result_v2.wrong = receive["wrong"]
        result_v2.test_time = receive["time"]
        if int(receive["total"]) < 96:
            result_v2.score = int(receive["right"])
        else:
            result_v2.score = float(receive["right"]) / float(receive["time"]) * 60
        result_v2.avg_speed = float(receive["right"]) * 60 / float(receive["time"])
        result_v2.save()
        return JsonResponse({"status": "success"})
    elif nid == 2:
        result_v3 = ExerciseV3Result(stu_account=dic["account"],name=name,grade=grade)
        result_v3.total_characters = int(receive["total"])
        result_v3.wrong_characters = len(receive["wrong"])
        result_v3.wrong = receive["wrong"]
        result_v3.judge_all = int(receive["judge_all"])
        result_v3.judge_right = int(receive["judge_right"])
        if result_v3.judge_all != 0:
            result_v3.judge_accuracy = float(result_v3.judge_right) / float(result_v3.judge_all)
        if result_v3.total_characters != 0:
            result_v3.accuracy_rate = 1 - float(result_v3.wrong_characters) / float(result_v3.total_characters)
        result_v3.test_time = int(receive["time"])
        result_v3.score = float(result_v3.total_characters - result_v3.wrong_characters) * 60 / float(result_v3.test_time)
        result_v3.avg_speed = float(result_v3.total_characters - result_v3.wrong_characters) * 60 / float(result_v3.test_time)
        result_v3.save()
        return JsonResponse({"status": "success"})



@csrf_exempt
def stu_turnToResult(request):
    if request.method == "POST":
        # print(request.POST)
        return JsonResponse({"status": True})


## 排行榜
def stu_ranklist(request, test=1):
    grade = request.session.get('info')['grade']
    if test == 1:
        queryset = models.ExerciseV1Result.objects.filter(grade=grade).order_by("-score")
    elif test == 2:
        queryset = models.ExerciseV2Result.objects.filter(grade=grade).order_by("-score")
    elif test == 3:
        queryset = models.ExerciseV3Result.objects.filter(grade=grade).order_by("-score")
    grade_arr = ["未知", "一年级", "二年级", "三年级", "四年级", "五年级", "六年级"]
    test_arr = ["未知", "阅读准确性测试", "阅读流畅性测试一", "阅读流畅性测试二"]

    page_object = Pagination(request, queryset)
    page_queryset = page_object.query_set
    page_string = page_object.html()

    context = {
        "grade": grade_arr[grade],
        "test": test_arr[test],
        "queryset": page_queryset,
        "page_string": page_string,
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


def stu_uploadTestTwo(request):
    if request.method == "POST":
        return JsonResponse({"error_message": True, "do_right": True})

@csrf_exempt
def get_exercise_list(request, nid=0):
    if nid == 0:
        grade = request.session.get('info')['grade']
        list = GenExerciseList(grade)
        return JsonResponse({"list": list})
    elif nid == 1:
        exercise_list = gen.getChart2()
        while len(exercise_list) < 96:
            exercise_list = gen.getChart2()
        return JsonResponse({"list": exercise_list})
    elif nid == 2:
        list = models.Exercise.objects.all()
        exercise_list = []
        for exercise in list:
            if len(exercise_list) > 60:
                break
            elem = {"content": exercise.content, "correct": exercise.answer}
            exercise_list.append(elem)
        random.shuffle(exercise_list)
        return JsonResponse({"list": exercise_list})
    elif nid == 3:
        # 返回词语列表，列表里每个元素是字典
        exercise_list = phrase.getPhrasesList()
        random.shuffle(exercise_list)
        return JsonResponse({"list": exercise_list})
    elif nid == 4:
        grade = request.session.get('info')['grade']
        exercise_list = gen.getChartOriginal()
        list = []
        for level in range(0, 6):
            for ch in exercise_list[level]:
                list.append(ch[0])
        random.shuffle(list)
        return JsonResponse({"character": list[0]})


from datetime import datetime
from reading_system.utils.character import check
@csrf_exempt
def stu_saveSpeech(request):
    file = request.FILES.get('file')
    wav_name = request.POST.get('wav_name')

    file_path = "reading_system/static/speech/" + wav_name + ".mp3"

    with open(file_path, 'wb') as f:
        f.write(file.read())

    return JsonResponse({"status": "success"} )
@csrf_exempt
def stu_recognizeSpeech(request, nid=0):
    dic = request.session.get('info')
    receive = request.POST

    # 识别音频
    file_name = receive["file_name"]
    mp3_path = 'reading_system/static/speech/' + file_name + '.mp3'
    recognize_path = 'reading_system/static/wav/' + file_name + '.wav'
    voice.mp3towav(mp3_path, 'reading_system/static/wav/');
    res = voice.recognize(recognize_path)
    res = check(res)

    # 识别测试音频
    if nid == 3:
        res2 = voice.recognize2(recognize_path)
        print(res2)
        if isinstance(res, str):
            return JsonResponse({"result": res, "success":True})
        else:
            return JsonResponse({"success":False})
    # 准确性测试模拟测试
    if nid == 4:
        if isinstance(res, str) and chinesecharacter.JudgeCharacter(res[0]):
            tar = receive["target"]
            msg = ""
            substr = res[1:]
            if CompareChar(tar, res[0]):
                # 第一个字识别正确
                if JudgePyInSentence(tar, substr):
                    msg = "回答正确，识别字正确且组词正确"
                else:
                    msg = "回答正确，识别字正确但组词错误"
            else:
                # 第一个字识别错误
                if JudgePyInSentence(tar, substr):
                    if IsSimilarChar(tar, res[0]):
                        msg = "正确，识别字错误但在允许范围内，组词正确"
                    else:
                        msg = "错误，识别字错误但组词正确"
                else:
                    msg = "错误，识别字错误且组词错误"
            return JsonResponse({"result": res, "success":True, "msg": msg})
        else:
            return JsonResponse({"success":False})

    # 存储识别结果
    wav_result = WavRecognitionResult(stu=dic['name'])
    wav_result.path = recognize_path
    wav_result.result = "error"
    if isinstance(res, str):
        wav_result.result = res
    wav_result.target = receive["character"]

    # 讯飞语音识别并存储识别结果
    rset = []
    if nid == 0 or nid == 2 or nid == 5:
        rset = ifly_recognize.recognize(recognize_path)
        for elem in rset:
            wav_result.result += ";" + elem
        rset.append(res)
        res = wav_result.result

    wav_result.save()

    grade = int(dic['grade'])

    err_msg = "err_msgerr_nosn"

    # 准确性测试
    if nid == 0:
        if isinstance(res, str):
            tar = receive["character"]
            again = False
            # 判断 目标汉字 和 候选集合的关系
            flag = chinesecharacter.JudgeSingleCharacter(tar,  rset)

            if not flag:
                # 存在 error_msg 则重新朗读
                if err_msg in rset:
                    again = True
                    return JsonResponse({"target": tar, "result": res, "right": flag, "again": again})

            # 所有年级统计结果
            if models.Character.objects.filter(character=tar).exists():
                row_object = models.Character.objects.get(character=tar)
                row_object.total_time = row_object.total_time + 1
                if flag:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()
            else:
                row_object = Character(character=tar, total_time=1, accurate_time=0)
                if flag:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()

            # 每个年级统计结果
            if models.CharacterOfGrade.objects.filter(character=tar,grade=grade).exists():
                row_object = models.CharacterOfGrade.objects.filter(character=tar,grade=grade).first()
                row_object.total_time = row_object.total_time + 1
                if flag:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()
            else:
                row_object = CharacterOfGrade(character=tar, grade=grade,total_time=1, accurate_time=0)
                if flag:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()

            return JsonResponse({"target": tar, "result": res, "right": flag, "again": again, })
        else:
            return JsonResponse({"target": tar, "result": "error", "right": False})

    elif nid == 1:
        if not isinstance(res, str):
            return JsonResponse({"result": "error"})
        tar = receive["character"]

        right = gen.compareSentenceRight(res, tar)
        cnt = gen.compareSentence(res, tar)

        wrong = ""
        for ch in tar:
            if not ch in right:
                wrong += ch
        
        for ch in tar:
            if models.Character.objects.filter(character=ch).exists():
                row_object = models.Character.objects.get(character=ch)
                row_object.total_time = row_object.total_time + 1
                if ch in right:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()
            else:
                row_object = Character(character=ch, total_time=1, accurate_time=0)
                if ch in right:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()
        return JsonResponse({"result": res, "cnt": cnt, "wrong": wrong, "len": len(tar)})
    elif nid == 2:
        # 阅读流畅性测试二
        if not isinstance(res, str):
            return JsonResponse({"result": "error"})
        tar = receive["character"]
        flag = receive["judge"]

        # 保存问题回答结果
        # 所有年级统计结果
        obj = models.Exercise.objects.get(content=tar)
        obj.total += 1
        if flag == obj.right:
            obj.right += 1
        if obj.total != 0:
            obj.accuracy = float(obj.right) / float(obj.total);
        obj.save()

        # 每个年级统计结果
        if models.ExerciseOfGrade.objects.filter(content=tar, grade=grade).exists():
            row_object = models.ExerciseOfGrade.objects.filter(content=tar, grade=grade).first()
            row_object.total = row_object.total + 1
            if flag == obj.right:
                row_object.right = row_object.right + 1
            row_object.accuracy = row_object.right / row_object.total
            row_object.save()
        else:
            row_object = ExerciseOfGrade(content=tar, grade=grade, total=1, right=0)
            if flag == obj.right:
                row_object.right = row_object.right + 1
            row_object.accuracy = row_object.right / row_object.total
            row_object.save()


        right = LCS_str(res, tar)
        cnt = LCS(res, tar)
        wrong = ""
        for ch in tar:
            if not ch in right:
                wrong += ch

        for ch in tar:
            if models.Character.objects.filter(character=ch).exists():
                row_object = models.Character.objects.get(character=ch)
                row_object.total_time = row_object.total_time + 1
                if ch in right:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()
            else:
                row_object = Character(character=ch, total_time=1, accurate_time=0)
                if ch in right:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()
        return JsonResponse({"result": res, "cnt": cnt, "wrong": wrong, "len": len(tar)})
    elif nid == 5:
        # 阅读流畅性测试一
        if not isinstance(res, str) or len(res) == 0:
            return JsonResponse({"result": "error"})

        ## 统计词语中读正确的汉字
        tar = receive["character"]
        right = LCS_str(res, tar)
        cnt = LCS(res, tar)
        wrong = ""
        phrase = receive["character"]

        ## 统计词语中读错的字
        for ch in tar:
            if not ch in right:
                wrong += ch

        ## 统计词语中每个汉字的正确率
        for ch in tar:
            if models.Character.objects.filter(character=ch).exists():
                row_object = models.Character.objects.get(character=ch)
                row_object.total_time = row_object.total_time + 1
                if ch in right:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()
            else:
                row_object = Character(character=ch, total_time=1, accurate_time=0)
                if ch in right:
                    row_object.accurate_time = row_object.accurate_time + 1
                row_object.accuracy = row_object.accurate_time / row_object.total_time
                row_object.save()

        ## 统计所有年级词语的正确率
        if models.Phrase.objects.filter(content=phrase).exists():
            row_object = models.Phrase.objects.get(content=phrase)
            if cnt == len(tar):
                row_object.right += 1
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            else:
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            row_object.save()
        else:
            row_object = Phrase(content=phrase, total=0, right=0)
            if cnt == len(tar):
                row_object.right += 1
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            else:
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            row_object.save()

        ## 统计对应年级词语的正确率
        if models.PhraseOfGrade.objects.filter(content=phrase, grade=grade).exists():
            row_object = models.PhraseOfGrade.objects.filter(content=phrase, grade=grade).first()
            if cnt == len(tar):
                row_object.right += 1
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            else:
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            row_object.save()
        else:
            row_object = PhraseOfGrade(content=phrase, grade=grade, total=0, right=0)
            if cnt == len(tar):
                row_object.right += 1
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            else:
                row_object.total += 1
                row_object.accuracy = row_object.right / row_object.total
            row_object.save()

        return JsonResponse({"result": res, "cnt": cnt, "wrong": wrong, "len": len(tar)})

def stu_showList(request, nid=1):
    dic = request.session.get('info')
    account = dic["account"]
    if nid == 1:
        queryset = models.ExerciseV1Result.objects.filter(stu_account=account).order_by("-exercise_time")
    elif nid == 2:
        queryset = models.ExerciseV2Result.objects.filter(stu_account=account).order_by("-exercise_time")
    elif nid == 3:
        queryset = models.ExerciseV3Result.objects.filter(stu_account=account).order_by("-exercise_time")
    page_object = Pagination(request, queryset)

    page_queryset = page_object.query_set
    page_string = page_object.html()
    context = {
        "queryset": page_queryset,
        "page_string": page_string,
    }
    if nid == 1:
        return render(request, "stu_listOne.html", context)
    elif nid == 2:
        return render(request, "stu_listTwo.html", context)
    elif nid == 3:
        return render(request, "stu_listThree.html", context)
    else:
        return redirect("/stu/home/")