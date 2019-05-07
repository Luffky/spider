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

class ZhihuPipeline(object):

    def __init__(self):
        self.file = codecs.open("question.json", mode='wb', encoding='utf-8')
        self.file2 = codecs.open("answer.json", mode='wb', encoding='utf-8')
        self.first = True


    def process_item(self, item, spider):
        line = ""
        if self.first:
            line = "the list: " + "\n"
            self.first = False


        if item.__class__.__name__ == 'ZhihuQuestionItem':
            question = {"name": item["name"], "url": item["url"], "keywords": item["keywords"],
                     "answer_count": item["answer_count"], "comment_count": item["comment_count"],
                     "flower_count": item["flower_count"], "date_created": item["date_created"]}

            line = line + json.dumps(question, ensure_ascii=False) + "\n"

            self.file.write(line)

        else:
            answer = {"title": item["title"], "author": item["author"], "ans_url": item["ans_url"], "comment_count": item["comment_count"],
                    "upvote_count": item["upvote_count"], "exceprt": item["excerpt"]
            }
            line = line + json.dumps(answer, ensure_ascii=False) + "\n"
            self.file2.write(line)

    def close_spider(self, spider):
        self.file.close()
        self.file2.close()