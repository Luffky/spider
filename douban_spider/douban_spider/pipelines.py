# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class DoubanSpiderPipeline(object):
    def __init__(self):
        self.file = codecs.open("douban_book_all.json", mode='wb', encoding='utf-8')
        self.first = True



    def process_item(self, item, spider):
        line = ""
        if self.first:
            line = "the list: " + "\n"
            self.first = False

        for i in range(len(item['star'])):

            movie = {"book_name": item["book_name"][i], "star": item["star"][i]}

            line = line + json.dumps(movie, ensure_ascii=False) + "\n"


        self.file.write(line)


    def close_spider(self, spider):
        self.file.close()
