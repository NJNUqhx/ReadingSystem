from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from reading_system.utils.chinesecharacter import characterLists


def SearchHome(request):
    return render(request, "search.html")


@csrf_exempt
def SearchCharacter(request):
    ch = request.POST.get('ch')
    res = characterLists.SearchCharacterToString(ch)
    dic = characterLists.SearchCharacter(ch)
    return JsonResponse({"res": res, "dict":dic})


@csrf_exempt
def SearchCharacterByComponent(request):
    component = request.POST.get('component')
    res = characterLists.SearchCharacterByComponent(component)
    return JsonResponse({"res": res})


@csrf_exempt
def SearchCharacterByPyin(request):
    pyin = request.POST.get('pyin')
    res = characterLists.SearchCharacterByPY(pyin)
    return JsonResponse({"res": res})
