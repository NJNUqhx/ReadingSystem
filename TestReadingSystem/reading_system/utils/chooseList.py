# from numpy import *
# import random
#
# from dataprepare import hanzi_dict
#
# def getExerciseList():
#     LISTNUM = 10
#     file1 = open('../static/character/2.txt', mode='r')
#     res = {}
#     while True:
#         a = file1.readline()
#         group = file1.readline()
#         if not a:
#             break
#         a = a.split(' ')
#         group = group.split(' ')
#         group = group[:-1]
#         for i in range(0, 3):
#             a[i] = float(a[i])
#         res[(a[0], a[1], a[2])] = group
#     resultList = []
#     groupnum = 0
#     for a in res:
#         i = a
#         group = res[a]
#         shenfu = []
#         choseshenfu = []
#         jiegou = [[], [], [], [], []]
#         jiegous = []
#         chosenjiegou = [0, 0, 0, 0, 0]
#         bihua = []
#         zipins = []
#         result = []
#         cnt = 0
#         groupnum += 1
#         for char in group:
#             feathers = hanzi_dict[char]
#             shenfu.append(feathers['声符'])
#             jiegous.append(int(feathers['结构方式']))
#             jiegou[int(feathers['结构方式'])].append(char)
#             bihua.append(int(feathers['笔画数']))
#             if isinstance(feathers['字频'], float):
#                 zipin = feathers['字频']
#             elif isinstance(feathers['字频'], str):
#                 str_list = feathers['字频'].split(';')
#                 zipin = str_list[0]
#             else:
#                 zipin = feathers['字频'][0]
#                 if isinstance(zipin, str):
#                     str_list = zipin.split(';')
#                     zipin = str_list[0]
#             zipin = float(zipin)
#             zipins.append(zipin)
#         meanbihua = mean(bihua)
#         stabihua = std(bihua)
#         while (cnt < LISTNUM):
#             idx = random.randint(0, len(group) - 1)
#             if group[idx] not in result:
#                 if bihua[idx] >= meanbihua - stabihua:
#                     if bihua[idx] <= meanbihua + stabihua:
#                         if zipins[idx] >= i[0] - i[1]:
#                             if zipins[idx] <= i[0] + i[1]:
#                                 if shenfu[idx] not in choseshenfu or shenfu[idx] == '':
#                                     if chosenjiegou[jiegous[idx]] <= round(
#                                             len(jiegou[jiegous[idx]]) * LISTNUM / len(group)):
#                                         result.append((group[idx], groupnum))
#                                         chosenjiegou[jiegous[idx]] += 1
#                                         choseshenfu.append(shenfu[idx])
#                                         cnt += 1
#         resultList.append(result)
#     return resultList