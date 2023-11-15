class PinYinTable:
    def __init__(self):
        self.table = {}
        self.ReadFromFile()

    def ReadFromFile(self):
        with open("reading_system/static/character/pinyin.txt", "r") as file:
            # 迭代文件对象，逐行读取文件内容
            for line in file:
                # 处理每一行内容
                content = line.strip()
                result = content.split(" ")
                elem = {"consonant": result[1], "vowel": result[2]}
                self.table[result[0]] = elem

    def GetConsonant(self, sound):
        if sound in self.table:
            return self.table[sound]["consonant"]
        else:
            return None

    def GetVowel(self, sound):
        if sound in self.table:
            return self.table[sound]["vowel"]
        else:
            return None

    def JudgeDifferentSounds(self, sound1, sound2):
        if self.GetConsonant(sound1) == self.GetConsonant(sound2):
            return True
        if self.GetVowel(sound1) == self.GetVowel(sound2):
            return True
        return False


pinyinTable = PinYinTable()
