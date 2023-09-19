from reading_system import models
from pypinyin import pinyin, Style
import openpyxl


def IsSimilarChar(ch1, ch2):
    sheng_diao1 = pinyin(ch1, style=Style(0), heteronym=True)[0]
    sheng_mu1 = pinyin(ch1, style=Style(3), heteronym=True)[0]
    yun_mu1 = pinyin(ch1, style=Style(5), heteronym=True)[0]

    sheng_diao2 = pinyin(ch2, style=Style(0), heteronym=True)[0]
    sheng_mu2 = pinyin(ch2, style=Style(3), heteronym=True)[0]
    yun_mu2 = pinyin(ch2, style=Style(5), heteronym=True)[0]

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
    # 返回 ch 的所有拼音含声调
    res = pinyin(ch, heteronym=True)
    return res[0]


def GetPinyin2(ch):
    # 返回 ch 的所有拼音不含声调
    sheng_diao = pinyin(ch, style=Style(0), heteronym=True)[0]
    return sheng_diao


def PinyinToStr(ch):
    res = GetPinyin(ch)
    s = ""
    for i in res:
        s = s + i + ";"
    return s


def CompareChar(ch1, ch2):
    if len(ch2) != 1:
        return False
    if not JudgeCharacter(ch2):
        return False
    # ch1 和 ch2 的拼音完全匹配
    py1 = GetPinyin(ch1)
    py2 = GetPinyin(ch2)
    for i in py1:
        if i in py2:
            return True
    return False


def JudgeCharacter(ch):
    return '\u4e00' <= ch <= '\u9fff'


def JudgePyInSentence(tar, sentence):
    # 查看目标汉字的拼音(不含声调)是否在句子中
    res1 = GetPinyin2(tar)
    for elem in res1:
        for ch in sentence:
            res2 = GetPinyin2(ch)
            if elem in res2:
                return True
    return False


def JudgePyInSentenceStrict(tar, sentence):
    # 查看目标汉字的拼音(不含声调)是否在句子中
    res1 = GetPinyin(tar)
    for elem in res1:
        for ch in sentence:
            res2 = GetPinyin(ch)
            if elem in res2:
                return True
    return False


def CompareChar2(tar, res):
    # 处理前面含有英文字母
    pyin = ""
    for ch in res:
        if ch.encode('utf-8').isalpha():
            pyin = pyin + ch
        else:
            break
    pyin = pyin.lower()
    sheng_diao = pinyin(tar, style=Style(0), heteronym=True)
    return pyin in sheng_diao[0]


def CheckCharacter(tar, sentence):
    if len(sentence) < 1:
        return False
    '''
        flag1: 判断单字的错误是否在允许范围内
        flag2: 判断单字的拼音是否在句子中
        flag3: 判断单字是否阅读正确
    '''
    flag1 = IsSimilarChar(tar, sentence[0])
    flag2 = JudgePyInSentence(tar, sentence)
    flag3 = CompareChar(tar, sentence[0]) or CompareChar2(tar, sentence)
    flag = flag3 or (flag1 and flag2)
    return flag


def GetErrorMsg(tar, res):
    substr = res[1:]
    flag1 = CompareChar(tar, res[0]) or CompareChar2(tar, res)
    if flag1:
        # 单字阅读正确
        if JudgePyInSentence(tar, substr):
            msg = "正确，单字阅读正确且组词正确"
        else:
            msg = "正确，单字阅读正确但组词错误"
    else:
        # 单字阅读错误
        if JudgePyInSentence(tar, substr):
            if IsSimilarChar(tar, res[0]):
                msg = "正确，单字阅读错误但在允许范围内且组词正确"
            else:
                msg = "错误，单字阅读错误，不在允许范围内但组词正确"
        else:
            msg = "错误，单字阅读错误且组词错误"
    return msg


class ChineseCharacter:
    def __init__(self):
        self.properties = [None] * 25
        self.dict = {}
        self.props = []
        self.index = 0

    def Output(self):
        print("------------------------------------------")
        print(self.index)
        for i in range(len(self.props)):
            print(self.dict[self.props[i]])

    def ToString(self):
        res = ""
        for i in range(len(self.props)):
            res = res + self.props[i].__str__() + ": " + self.dict[self.props[i]].__str__() + "\n"
        return res


class CharacterLists:
    def __init__(self):
        # 存储所有汉字对象的数组
        # 汉字对象的个数
        self.num = 0
        self.characters = []

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

        self.characters = [ChineseCharacter() for i in range(self.num)]

        props = []

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
            self.characters[idx].index = idx

    def Output(self):
        print(len(self.characters))
        for i in range(len(self.characters)):
            if i % 100 == 0:
                print(self.characters[i].dict)

    def SearchCharacter(self, ch):
        if len(ch) != 1:
            return None
        for elem in self.characters:
            if elem.dict["汉字"] == ch:
                return elem.dict
        return None

    def SearchCharacterToString(self, ch):
        if len(ch) != 1:
            return None
        for elem in self.characters:
            if elem.dict["汉字"] == ch:
                return elem.ToString()
        return None

    def SearchCharacterByComponent(self, component):
        res = ""
        if len(component) != 1:
            return res
        for elem in self.characters:
            list1 = elem.dict["具体的部件(一级)"]
            list2 = elem.dict["具体的部件(二级)"]
            list3 = elem.dict["具体的部件(三级)"]
            if list1 and component in list1:
                res += elem.dict["汉字"]
                continue
            if list2 and component in list2:
                res += elem.dict["汉字"]
                continue
            if list3 and component in list3:
                res += elem.dict["汉字"]
                continue
        return res

    def SearchCharacterByPY(self, pyin):
        res = ""
        for elem in self.characters:
            s = elem.dict["拼音"]
            idx = s.find(pyin)
            if idx == -1:
                continue
            last = idx + len(pyin)
            if last >= len(s) or not s[last].__str__().isalpha():
                res += elem.dict["汉字"]
        return res


def LCS(str1, str2):
    # 返回最大公共子串长度
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    max_len = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if CompareChar(str1[i - 1], str2[j - 1]):
                dp[i][j] = dp[i - 1][j - 1] + 1
                if max_len < dp[i][j]:
                    max_len = dp[i][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return max_len


def LCS_str(str1, str2):
    # 返回最大公共子串
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    tr = [[0] * (n + 1) for _ in range(m + 1)]
    '''
    1: 斜向上
    2: 向左
    3: 向上
    '''
    max_len = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if CompareChar(str1[i - 1], str2[j - 1]):
                dp[i][j] = dp[i - 1][j - 1] + 1
                tr[i][j] = 1
                if max_len < dp[i][j]:
                    max_len = dp[i][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                if dp[i][j] == dp[i - 1][j]:
                    tr[i][j] = 3
                else:
                    tr[i][j] = 2

    res = ""
    i = m
    j = n
    while i and j:
        if tr[i][j] == 0:
            break
        elif tr[i][j] == 1:
            res = str1[i - 1] + res
            i -= 1
            j -= 1
        elif tr[i][j] == 2:
            j -= 1
        else:
            i -= 1
    return res


def TransDigit(s):
    for i in range(len(s)):
        if str.isdigit(s[i]):
            for j in range(i, len(s)):
                if not str.isdigit(s[j]):
                    print(s[i: j])
                    digit = s[i: j]
                    Dict = DigitDict()
                    s = s.replace(digit, Dict[digit])
                    return s


def DigitDict():
    file_name = "reading_system/static/character/digits.txt"
    dict = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        while True:
            s = f.readline()
            if not s:
                break
            idx = s.find(':')
            digit = s[0:idx]
            hanzi = s[idx + 1:-1]
            dict[digit] = hanzi
    return dict


characterLists = CharacterLists()
