from reading_system import models
from pypinyin import pinyin, Style
import openpyxl
import time


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


def IsSimilarChar(ch1, ch2):
    sheng_diao1 = pinyin(ch1, style=Style(0), heteronym=True)
    sheng_mu1 = pinyin(ch1, style=Style(3), heteronym=True)
    yun_mu1 = pinyin(ch1, style=Style(5), heteronym=True)

    sheng_diao2 = pinyin(ch2, style=Style(0), heteronym=True)
    sheng_mu2 = pinyin(ch2, style=Style(3), heteronym=True)
    yun_mu2 = pinyin(ch2, style=Style(5), heteronym=True)

    # print(sheng_diao1, sheng_mu1, yun_mu1)
    # print(sheng_diao2, sheng_mu2, yun_mu2)

    flag1, flag2, flag3 = False, False, False

    for elem in sheng_diao1:
        if elem in sheng_diao2:
            flag1 = True
            break

    for elem in sheng_mu1:
        if elem in sheng_mu2:
            flag2 = True

    for elem in yun_mu1:
        if elem in yun_mu2:
            flag3 = True
    return flag1 or flag2 or flag3


def JudgeCharacter(ch):
    return '\u4e00' <= ch <= '\u9fff'


# class ChineseCharacter:
#     def __init__(self):
#         self.properties = [None] * 25
#         self.dict = {}
#         self.props = []
#
#     def Output(self):
#         for i in range(len(self.props)):
#             print(self.props[i], ":", self.dict[self.props[i]])
#
#
# class CharacterLists:
#     def __init__(self):
#         excel_path = "reading_system/static/character/characters.xlsx"
#         wb = openpyxl.load_workbook(excel_path)
#         ws = wb.active
#
#         lines = []
#         for line in ws:
#             lines.append(line)
#
#         self.characters = [ChineseCharacter()] * len(lines[0])
#
#         cols = len(lines[0])
#         rows = len(lines)
#
#         props = []
#
#         for i in range(rows):
#             props.append(lines[i][1].value)
#
#         print(props)
#
#         cc = 10
#
#         for i in range(2, cc):
#             self.characters[i].props = props
#
#             for j in range(rows):
#                 self.characters[i].properties[j] = lines[j][i].value
#                 self.characters[i].dict[props[j]] = lines[j][i].value
#
#             print(self.characters[i].dict['汉字'])
#
#         for i in range(2, cc):
#             print(self.characters[i].dict['汉字'])
#
#     # 按部件搜索
#     def SearchCharacterByComponent(self, component):
#         pass
#
#     def SearchCharacterByPinyin(self, piny):
#         pass
#
#     def SearchCharacter(self, ch):
#         for elem in self.characters:
#             # print(elem.dict['汉字'])
#             if elem.dict['汉字'] == ch:
#                 return elem.dict
#
#
# def test0():
#     excel_path = "reading_system/static/character/characters.xlsx"
#     wb = openpyxl.load_workbook(excel_path)
#     ws = wb.active
#     cnt = 0
#     lines = []
#     for line in ws:
#         lines.append(line)
#
#
# def test1():
#     chs = CharacterLists()
#     chs.SearchCharacter('天')
#
#
# test1()

#
#
def TestExcel():
    # 初始化表格
    cur_time = time.time().__str__()
    excel_path = "reading_system/static/result/result" + cur_time + ".xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Excel'
    ws['A1'] = '目标汉字'
    ws['B1'] = '识别结果'
    ws['C1'] = '判断结果'
    ws['D1'] = '测试时间'
    ws['E1'] = '学生账号'
    result = models.WavRecognitionResult.objects.all()
    row = 2
    for obj in result:
        tar = obj.target
        res = obj.result

        ws.cell(row, 1).value = tar
        ws.cell(row, 2).value = res

        substr = res[1:]
        if CompareChar(tar, res[0]):
            # 第一个字识别正确
            if JudgePyInSentence(tar, substr):
                msg = "正确，识别字正确且组词正确"
            else:
                msg = "正确，识别字正确但组词错误"
        else:
            # 第一个字识别错误
            if IsSimilarChar(tar, res[0]) and JudgePyInSentence(tar, substr):
                msg = "正确，识别字错误但在允许范围内，组词正确"
            else:
                msg = "错误，识别字错误且组词错误"
        ws.cell(row, 3).value = msg
        ws.cell(row, 4).value = obj.exercise_time.__str__()
        ws.cell(row, 5).value = obj.stu
        row += 1
    wb.save(excel_path)


def CheckCharacter(tar, sentence):
    if not JudgeCharacter(sentence[0]):
        return False
    flag1 = IsSimilarChar(tar, sentence[0])
    flag2 = JudgePyInSentence(tar, sentence)
    flag3 = CompareChar(tar, sentence[0])
    flag = flag3 or (flag1 and flag2)
    return flag


def JudgePyInSentence(tar, sentence):
    res1 = GetPinyin(tar)
    for elem in res1:
        for ch in sentence:
            res2 = GetPinyin(ch)
            if elem in res2:
                return True
    return False


TestExcel()
# print(JudgePyInSentence('披', '拼披萨'))
