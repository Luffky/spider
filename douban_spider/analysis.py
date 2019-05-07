#coding=utf-8
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

file = codecs.open("douban_book_all.json", mode='r', encoding='utf-8')
k = file.readlines()

l = list()
for i in k:
    l.append(json.loads(i))

l = sorted(l, key=lambda a: a["star"])

file2 = codecs.open("douban_allbooks_sorted.json", mode="wb", encoding='utf-8')
for i in l:
    file2.write(json.dumps(i, ensure_ascii=False) + "\n")



file.close()



