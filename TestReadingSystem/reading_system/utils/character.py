def check(s):
    res = ""
    for ch in s:
        if ch == u'一':
            ch = u'衣'
        elif ch == u'滚':
            ch = u'衮'
        res += ch
    return res