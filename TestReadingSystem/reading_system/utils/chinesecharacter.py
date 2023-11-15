import copy

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


# 辅助进行字符串比较
def LCS(str1, str2):
    # 返回最大公共子串长度
    str1 = TransDigit(str1)
    str2 = TransDigit(str2)
    m = len(str1)
    n = len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    max_len = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if CompareSingleCharacter(str1[i - 1], str2[j - 1]):
                dp[i][j] = dp[i - 1][j - 1] + 1
                if max_len < dp[i][j]:
                    max_len = dp[i][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return max_len


def LCS_str(str1, str2):
    # 返回最大公共子串
    str1 = TransDigit(str1)
    str2 = TransDigit(str2)
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
            if CompareSingleCharacter(str1[i - 1], str2[j - 1]):
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


def TransDigit(num):
    chinese_dict = {
        '0': '零',
        '1': '一',
        '2': '二',
        '3': '三',
        '4': '四',
        '5': '五',
        '6': '六',
        '7': '七',
        '8': '八',
        '9': '九',
    }

    def convert_chunk(chunk):
        chunk_str = str(chunk)
        length = len(chunk_str)
        result = ''
        if length == 1:
            result += chinese_dict[chunk_str]
        elif length == 2:
            if chunk_str[0] == '1':
                if chunk_str[1] == '0':
                    result += '十'
                else:
                    result += '十' + chinese_dict[chunk_str[1]]
            else:
                if chunk_str[1] == '0':
                    result += chinese_dict[chunk_str[0]] + '十'
                else:
                    result += chinese_dict[chunk_str[0]] + '十' + chinese_dict[chunk_str[1]]
        elif length == 3:
            if chunk_str[1:] == '00':
                result += chinese_dict[chunk_str[0]] + '百'
            else:
                result += chinese_dict[chunk_str[0]] + '百' + convert_chunk(int(chunk_str[1:]))
        elif length == 4:
            if chunk_str[1:] == '000':
                result += chinese_dict[chunk_str[0]] + '千'
            else:
                result += chinese_dict[chunk_str[0]] + '千' + convert_chunk(int(chunk_str[1:]))
        return result

    result = ''
    current_chunk = ''
    for char in num:
        if char.isdigit():
            current_chunk += char
        else:
            if current_chunk:
                result += convert_chunk(int(current_chunk))
                current_chunk = ''
            result += char

    if current_chunk:
        result += convert_chunk(int(current_chunk))

    return result


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


# 将字典写入文件中
def write_dict_to_file(dictionary, filename):
    import json
    with open(filename, 'w') as file:
        for key, value in dictionary.items():
            file.write(json.dumps({key: value}, ensure_ascii=False) + '\n')


# 获取所有汉字的拼音字典
def GetDict(chLists):
    import re
    pyDict = {}
    for elem in chLists.characters:
        # print(elem.dict["汉字"])
        # print(elem.dict["拼音"])
        pyin = elem.dict["拼音"]
        pyinset = re.split(",|;", pyin)
        pyinset = [x for x in pyinset if not x.isdigit()]
        pyDict[elem.dict["汉字"]] = pyinset
    write_dict_to_file(pyDict, "reading_system/static/character/pydict.txt")
    return pyDict


pyinDict = GetDict(characterLists)


# 获取给定汉字的拼音集合
def GetPinyinVec(ch):
    import re
    if ch in pyinDict:
        vec = pyinDict[ch]
        res = []
        for elem in vec:
            new_elem = re.sub(r'\d+', '', elem)
            res.append(new_elem)
    else:
        res = GetPinyin2(ch)
    return res


# 判断两个汉字是否在可允许的错误范围内
def JudgeBetweenCharacters(ch1, ch2):
    from reading_system.utils.PinYin import pinyinTable
    vec1 = GetPinyinVec(ch1)
    vec2 = GetPinyinVec(ch2)
    for elem1 in vec1:
        for elem2 in vec2:
            if pinyinTable.JudgeDifferentSounds(elem1, elem2):
                return True
    return False


# 获取准确性测试题目
def GenExerciseList(grade):
    from reading_system.utils.chooseList import gen
    import random
    list = []
    while len(list) < 100:
        exercise_list = gen.getChartOriginal()
        if 1 <= grade <= 2:
            # 对应难度 1 2 3 4 5 6
            for level in range(0, 6):
                for ch in exercise_list[level]:
                    elem = {"ch": ch[0], "level": ch[1]}
                    if elem not in list:
                        list.append(elem)
        else:
            for level in range(1, 10):
                for ch in exercise_list[level]:
                    elem = {"ch": ch[0], "level": ch[1]}
                    if elem not in list:
                        list.append(elem)
    random.shuffle(list)
    return list


# 处理识别结果，转化为list
def SplitWavResult(wav_result):
    rset = wav_result.split(";")
    return rset


# 比较两个汉字是否相同
def CompareSingleCharacter(tar, src):
    if len(src) != 1 or not JudgeCharacter(src):
        return False
    if tar in pyinDict:
        list1 = pyinDict[tar]
    else:
        list1 = GetPinyin(tar)
    if src in pyinDict:
        list2 = pyinDict[src]
    else:
        list2 = GetPinyin(src)
    for elem in list1:
        if elem in list2:
            return True
    return False


# 根据拼音字典，查看汉字读音是否在句子中
def CompareSingleCharacterInSentence(tar, src):
    for ch in src:
        if not JudgeCharacter(ch):
            continue
        flag = CompareSingleCharacter(tar, ch)
        if flag:
            return True
    return False


# 判断单个汉字的正确性，rset为候选结果的集合
def JudgeSingleCharacter(tar, rset):
    for elem in rset:
        flag = False
        if len(elem) == 1:
            flag = CompareSingleCharacter(tar, elem)
        elif len(elem) > 1:
            flag = CompareSingleCharacterInSentence(tar, elem) and JudgeBetweenCharacters(tar, elem[0])
        if flag:
            return True
    return False


def GetErrorMessage(tar, res):
    # 获取阅读准确性、阅读流畅性测试错误信息
    rset = SplitWavResult(res)
    msg = "error"
    if len(tar) == 1:
        # 阅读准确性测试
        for elem in rset:
            if len(elem) == 1:
                # 直接朗读汉字
                if CompareSingleCharacter(tar, elem):
                    msg = "朗读正确，" + tar + " 与 " + elem + "读音相同"
                    return msg
                else:
                    msg = "朗读错误，" + tar + " 与 " + elem + "读音不同"
            elif len(elem) > 1:
                # 朗读该字并组词
                if JudgeCharacter(elem[0]):
                    if CompareSingleCharacter(tar, elem[0]):
                        msg = "朗读正确，" + tar + " 与 " + elem[0] + "读音相同"
                        return msg
                    if JudgeBetweenCharacters(tar, elem[0]):
                        # 查看第一个字是否在允许范围内
                        if CompareSingleCharacterInSentence(tar, elem[1:]):
                            msg = "朗读正确，" + tar + " 在词语 " + elem[1:] + " 中"
                            return msg
                        else:
                            msg = "朗读错误，" + tar + " 不在词语 " + elem[1:] + " 中"
                    else:
                        msg = "朗读错误，" + tar + " 与 " + elem[0] + " 超过允许的错误范围"
                else:
                    msg = "识别错误，" + elem[0] + " 不是汉字"
    else:
        # 阅读流畅性测试
        lcs_len = LCS(tar, res)
        lcs_str = LCS_str(tar, res)
        if lcs_len == 0:
            msg = "朗读完全错误"
        elif lcs_len == len(tar):
            msg = "朗读完全正确"
        else:
            msg = "朗读部分正确，正确部分：" + lcs_str
    return msg
