import random
import xlrd
import datetime
import re
import pandas as pd
from numpy import *
from pypinyin import pinyin
from reading_system.utils.chinesecharacter import LCS, LCS_str, TransDigit

LISTNUM = 10


class Gen_chart:
    def change_LISTNUM(self, num):
        self.LISTNUM = num

    def excel_to_dict(self, filename, **kwargs):
        df = pd.read_excel(filename)
        hanzi_list = df['汉字'].tolist()
        """
        excel转dict

        1.传来的文件可以是文件路径，也可以是二进制文件
        2.传来的可以是二进制文件，这里以django接收前端传来文件为例：
            接收用 request.FILES.get("fileName", None) 传入 my_file 即可

        kwargs接收的参数有:
            _sheet索引，0代表第一个表，1代表第二个表，默认0
            _max表格最大的行数，默认2000行
            _min表格最小的行数，默认1行
        """
        # excel 文件
        excel_file = filename
        # sheet 索引
        _sheet = kwargs.get("sheet", 0)
        # max 最大条数
        _max = kwargs.get("max", 5000)
        # min 最小条数
        _min = kwargs.get("min", 0)

        # 判断是否为文件路径
        # if os.path.exists(excel_file):
        workbook = xlrd.open_workbook(excel_file)
        # else:
        # 上传的文件不保存，直接在内存中读取文件
        # workbook = xlrd.open_workbook(filename=str(excel_file), file_contents=excel_file.read())

        # 根据sheet索引或者名称获取sheet内容
        data_sheet = workbook.sheets()[_sheet]
        # 获取sheet名称，行数，列数据
        sheet_name = data_sheet.name
        sheet_nrows = data_sheet.nrows
        sheet_ncols = data_sheet.ncols

        # 文件记录不得大于2000条
        if sheet_nrows > _max:
            return {"code": "0001", "msg": "文件记录大于{}条，请联系管理员上传".format(_max), "data": None}

        # 判断是否为空数据
        if sheet_nrows <= _min:
            return {"code": "0001", "msg": "空数据表格,停止导入", "data": None}

        # excel转dict
        get_data = []
        hanzi_dict = {}
        for i in range(1, sheet_nrows):
            # 定义一个空字典
            sheet_data = {}
            for j in range(sheet_ncols):
                # 获取单元格数据类型
                c_type = data_sheet.cell(i, j).ctype
                # 获取单元格数据
                c_cell = data_sheet.cell_value(i, j)
                # print(c_type)
                if c_type == 1:
                    # print(type(c_cell))
                    c_cell = re.split(r'[；、,]', c_cell)
                elif c_type == 2 and c_cell % 1 == 0:  # 如果是整形
                    c_cell = int(c_cell)
                elif c_type == 3:
                    # 转成datetime对象
                    c_cell = datetime(*xlrd.xldate_as_tuple(c_cell, 0)).strftime('%Y-%m-%d %H:%M:%S')
                elif c_type == 4:
                    c_cell = True if c_cell == 1 else False
                sheet_data[data_sheet.row_values(0)[j]] = c_cell
                # 循环每一个有效的单元格，将字段与值对应存储到字典中
                # 字典的key就是excel表中每列第一行的字段
                # sheet_data[self.keys[j]] = self.table.row_values(i)[j]
            # 再将字典追加到列表中
            hanzi_dict[hanzi_list[i - 1]] = sheet_data
            get_data.append(sheet_data)
        # 返回从excel中获取到的数据：以列表存字典的形式返回
        return hanzi_dict

    def __init__(self, file1, file2):
        self.res = {}
        self.charList = []
        self.pinyindic = {}
        self.hanzi_dict2 = {}
        self.hanzi_dict2 = self.excel_to_dict(file2)
        self.LISTNUM = 10
        dict_key_ls = list(self.hanzi_dict2.keys())
        random.shuffle(dict_key_ls)
        hanzi_dict = {}
        for key in dict_key_ls:
            hanzi_dict[key] = self.hanzi_dict2.get(key)

        charlists = []
        charlists2 = []
        chars = []

        # 声符 结构方式 笔画数
        for char in hanzi_dict:
            feathers = hanzi_dict[char]
            self.pinyindic[char] = []
            charlist = []
            charlist2 = []
            featherlist = []
            if isinstance(feathers['字频'], float):
                zipin = feathers['字频']
            elif isinstance(feathers['字频'], str):
                str_list = feathers['字频'].split(';')
                zipin = str_list[0]
            else:
                zipin = feathers['字频'][0]
                if isinstance(zipin, str):
                    str_list = zipin.split(';')
                    zipin = str_list[0]
            if isinstance(feathers['汉字在课本中首次出现的册数'], int):
                ceshu = feathers['汉字在课本中首次出现的册数']
            elif isinstance(feathers['汉字在课本中首次出现的册数'], str):
                ceshu = feathers['汉字在课本中首次出现的册数'].split(';')
                ceshu = ceshu[0]
            else:
                ceshu = feathers['汉字在课本中首次出现的册数'][0]
            if len(feathers['拼音']) == 2:
                self.pinyindic[char].append(feathers['拼音'][1])
            else:
                pinyins = feathers['拼音'][1].split(';')
                self.pinyindic[char].append(pinyins[0])
                self.pinyindic[char].append(feathers['拼音'][2])
            if zipin != '':
                if (float(zipin) == 0):
                    charlist.append(float('-inf'))
                    charlist2.append(float(zipin))
                else:
                    charlist.append(log(float(zipin)))
                    charlist2.append(float(zipin))
                charlist.append(log(int(ceshu)))
                charlist2.append(int(ceshu))
                # charlist.append(float(zipin))
                # charlist.append(int(ceshu))
                chars.append(char)
                charlists.append(charlist)
                charlists2.append(charlist2)
                #        if (float(zipin) == 0) :
                #    charlist.append(float('-inf'))
                # else:
                #    charlist.append(log(float(zipin)))
                # charlist.append(log(int(ceshu)))

        # file1 = open('C:/Users/non-fire/Desktop/词表/2.txt', mode='r')
        while True:
            a = file1.readline()
            group = file1.readline()
            if not a:
                break
            a = a.split(' ')
            group = group.split(' ')
            group = group[:-1]
            for i in range(0, 3):
                a[i] = float(a[i])
            self.res[(a[0], a[1], a[2])] = group

    # 比较汉字
    def compareChar(self, ch1, ch2):
        list1 = pinyin(ch1, heteronym=True)[0]
        list2 = pinyin(ch2, heteronym=True)[0]
        for elem in list1:
            if elem in list2:
                return True
        return False

    def compareSentenceRight(self, str1, str2):
        str1 = TransDigit(str1)
        return LCS_str(str1, str2)

    # 比较句子
    def compareSentence(self, str1, str2):
        return LCS(str1, str2)

    # 阅读流畅性测试1
    def getChart2(self):
        cnt = 0
        for a in self.res:
            group = self.res[a]
            cnt += 1
            if (cnt > 2):
                break
            i = 0
            while i < 48:
                idx = random.randint(0, len(group) - 1)
                if group[idx] not in self.charList:
                    self.charList.append(group[idx])
                    i += 1
        return self.charList

    def getChart(self):
        self.resultList = []
        groupnum = 0
        for a in self.res:
            i = a
            group = self.res[a]
            shenfu = []
            choseshenfu = []
            jiegou = [[], [], [], [], []]
            jiegous = []
            chosenjiegou = [0, 0, 0, 0, 0]
            bihua = []
            zipins = []
            result = []
            cnt = 0
            groupnum += 1
            for char in group:
                feathers = self.hanzi_dict2[char]
                shenfu.append(feathers['声符'])
                jiegous.append(int(feathers['结构方式']))
                jiegou[int(feathers['结构方式'])].append(char)
                bihua.append(int(feathers['笔画数']))
                if isinstance(feathers['字频'], float):
                    zipin = feathers['字频']
                elif isinstance(feathers['字频'], str):
                    str_list = feathers['字频'].split(';')
                    zipin = str_list[0]
                else:
                    zipin = feathers['字频'][0]
                    if isinstance(zipin, str):
                        str_list = zipin.split(';')
                        zipin = str_list[0]
                zipin = float(zipin)
                zipins.append(zipin)
            meanbihua = mean(bihua)
            stabihua = std(bihua)
            while (cnt < self.LISTNUM):
                idx = random.randint(0, len(group) - 1)
                if group[idx] not in result:
                    if bihua[idx] >= meanbihua - stabihua:
                        if bihua[idx] <= meanbihua + stabihua:
                            if zipins[idx] >= i[0] - i[1]:
                                if zipins[idx] <= i[0] + i[1]:
                                    if shenfu[idx] not in choseshenfu or shenfu[idx] == '':
                                        if chosenjiegou[jiegous[idx]] <= round(
                                                len(jiegou[jiegous[idx]]) * self.LISTNUM / len(group)):
                                            # result.append((group[idx], groupnum))
                                            result.append(group[idx])
                                            chosenjiegou[jiegous[idx]] += 1
                                            choseshenfu.append(shenfu[idx])
                                            cnt += 1
            self.resultList.append(result)
        return self.resultList

    def getChartOriginal(self):
        resultList = []
        groupnum = 0
        for a in self.res:
            i = a
            group = self.res[a]
            shenfu = []
            choseshenfu = []
            jiegou = [[], [], [], [], []]
            jiegous = []
            chosenjiegou = [0, 0, 0, 0, 0]
            bihua = []
            zipins = []
            result = []
            cnt = 0
            groupnum += 1
            for char in group:
                feathers = self.hanzi_dict2[char]
                shenfu.append(feathers['声符'])
                jiegous.append(int(feathers['结构方式']))
                jiegou[int(feathers['结构方式'])].append(char)
                bihua.append(int(feathers['笔画数']))
                if isinstance(feathers['字频'], float):
                    zipin = feathers['字频']
                elif isinstance(feathers['字频'], str):
                    str_list = feathers['字频'].split(';')
                    zipin = str_list[0]
                else:
                    zipin = feathers['字频'][0]
                    if isinstance(zipin, str):
                        str_list = zipin.split(';')
                        zipin = str_list[0]
                zipin = float(zipin)
                zipins.append(zipin)
            meanbihua = mean(bihua)
            stabihua = std(bihua)
            while (cnt < LISTNUM):
                idx = random.randint(0, len(group) - 1)
                if group[idx] not in result:
                    if bihua[idx] >= meanbihua - stabihua:
                        if bihua[idx] <= meanbihua + stabihua:
                            if zipins[idx] >= i[0] - i[1]:
                                if zipins[idx] <= i[0] + i[1]:
                                    if shenfu[idx] not in choseshenfu or shenfu[idx] == '':
                                        if chosenjiegou[jiegous[idx]] <= round(
                                                len(jiegou[jiegous[idx]]) * LISTNUM / len(group)):
                                            result.append((group[idx], groupnum))
                                            chosenjiegou[jiegous[idx]] += 1
                                            choseshenfu.append(shenfu[idx])
                                            cnt += 1
            resultList.append(result)
        return resultList


file = 'reading_system/static/character/hanzi1.xlsx'
gen = Gen_chart(open('reading_system/static/character/2.txt', mode='r', encoding='gbk'), file)
