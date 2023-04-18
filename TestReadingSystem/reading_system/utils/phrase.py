class Phrase:
    def __init__(self):
        self.phrases = []
        self.read()

    def read(self):
        with open('reading_system/static/character/phrases.txt', encoding='utf-8') as file_obj:
            for line in file_obj:
                clean_obj = line.rstrip()
                if len(clean_obj):
                    elem = {"phrase": clean_obj, "len": len(clean_obj)}
                    self.phrases.append(elem)


    def output(self):
        print(self.phrases)
        print(len(self.phrases))

    def getPhrasesList(self):
        return self.phrases


phrase = Phrase()
