from django.test import TestCase
from reading_system.utils.chooseList import gen

hash_set = gen.res
cnt = 0
target = []
for key in hash_set.keys():
    print(type(hash_set[key]))
    target.append(hash_set[key])
    print(len(hash_set[key]))
    cnt += 1
    if cnt == 2:
        break
print(len(target[0])+len(target[1]))

# 写入所有目标汉字
# write_file = open('D:/GitHub/ReadingSystem/TestReadingSystem/target.txt', mode="a", encoding='utf-8')
# write_file.writelines(target[0])
# write_file.writelines(target[1])
# write_file.close()

write_file = open('D:/GitHub/ReadingSystem/TestReadingSystem/not_qualified.txt', mode="a", encoding='utf-8')


file = open('D:/GitHub/ReadingSystem/TestReadingSystem/test.txt', mode='r', encoding='utf-8')
linelist = file.readlines()
file.close()
for line in linelist:
    for ch in line:
        if '\u4e00' <= ch <= '\u9fff':
            if ch in target[0] or ch in target[1]:
                continue
            else:
                print(ch + "不在目标汉字范围中")
                print(line)
                write_file.write(ch + ": " + line)
                break

write_file.close()


