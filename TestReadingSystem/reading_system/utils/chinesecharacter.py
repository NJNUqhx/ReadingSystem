from reading_system import models
from pypinyin import pinyin, Style
import openpyxl

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


def JudgeCharacter(ch):
    return '\u4e00' <= ch <= '\u9fff'


def CheckCharacter(tar, sentence):
    if not JudgeCharacter(sentence[0]):
        return False
    flag1 = IsSimilarChar(tar, sentence[0])
    flag2 = tar in sentence
    flag3 = CompareChar(tar, sentence[0])
    flag = flag3 or (flag1 and flag2)
    return flag


class ChineseCharacter:
    def __init__(self):
        self.properties = [None] * 25
        self.dict = {}
        self.props = []

    def Output(self):
        for i in range(len(self.props)):
            print(self.dict[self.props[i]])


class CharacterLists:
    def __init__(self):
        # 存储所有汉字对象的数组
        # 汉字对象的个数
        self.num = 0

        excel_path = "reading_system/static/character/characters.xlsx"
        wb = openpyxl.load_workbook(excel_path)
        ws = wb.active

        lines = []
        for line in ws:
            lines.append(line)

        valid_col = []

        for idx in range(len(lines[0])):
            ch = lines[0][idx].value.__str__()
            if '\u4e00' <= ch <= '\u9fff':
                self.num += 1
                valid_col.append(idx)
        self.characters = [ChineseCharacter()] * self.num

        props = []

        idx = 0
        # 第 i 行 -> 第 i 个属性
        for i in range(len(lines)):
            props.append(lines[i][1].value)
            # 第 j - 2 个汉字的属性
            idx = 0
            for j in range(len(lines[i])):

                # 跳过不是汉字的列
                if j not in valid_col:
                    continue
                self.characters[idx].properties[i] = lines[i][j].value
                self.characters[idx].dict[props[i]] = lines[i][j].value
                idx += 1

        for idx in range(self.num):
            self.characters[idx].props = props

    def SearchCharacter(self, ch):
        pass
