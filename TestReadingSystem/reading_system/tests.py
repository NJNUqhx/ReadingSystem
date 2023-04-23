from reading_system import models
from pypinyin import pinyin
import openpyxl


def GetPinyin(ch):
    res = pinyin(ch, heteronym=True)
    return res[0]


def PinyinToStr(ch):
    res = GetPinyin(ch)
    s = ""
    for i in res:
        s = s + i + ";"
    return s


def CompareChar(ch1, ch2):
    py1 = GetPinyin(ch1)
    py2 = GetPinyin(ch2)
    for i in py1:
        if i in py2:
            return True
    return False


def TestExcel():
    excel_path = "reading_system/static/result/result.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Excel'
    ws['A1'] = '目标汉字'
    ws['B1'] = '目标汉字读音'
    ws['C1'] = '识别汉字'
    ws['D1'] = '识别汉字读音'

    ws.cell(2, 1).value = "长"
    ws.cell(2, 2).value = PinyinToStr("长")
    ws.cell(2, 3).value = "涨"
    ws.cell(2, 4).value = PinyinToStr("涨")

    wb.save(excel_path)

#初始化表格
excel_path = "reading_system/static/result/result.xlsx"
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Excel'
ws['A1'] = '目标汉字'
ws['B1'] = '目标汉字读音'
ws['C1'] = '识别汉字'
ws['D1'] = '识别汉字读音'
result = models.WavRecognitionResult.objects.all()
row = 2
for obj in result:
    tar = obj.target
    res = obj.result
    if len(tar) != 1 or len(res) != 1 or CompareChar(tar, res):
        continue
    ws.cell(row, 1).value = tar
    ws.cell(row, 2).value = PinyinToStr(tar)
    ws.cell(row, 3).value = res
    ws.cell(row, 4).value = PinyinToStr(res)
    row += 1
wb.save(excel_path)
