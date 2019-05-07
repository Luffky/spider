from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from zhihu.items import ZhihuAnswerItem, ZhihuQuestionItem
import re
import json

from zhihu.settings import *

class ZhihuLoginSpider(CrawlSpider):
    name = "zhihu"
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/people/fu-kai-yu-48/activities']

    download_delay=0.5

    capacha_index = [
        [12.95, 14.969999999999998],
        [36.1, 16.009999999999998],
        [57.16, 24.44],
        [84.52, 19.17],
        [108.72, 28.64],
        [132.95, 24.44],
        [151.89, 23.380000000000002]
    ]

    # next_page = "https://www.zhihu.com/api/v3/feed/topstory?action_feed=True&limit=7" \
    #             "&session_token={0}&action=down&after_id={1}&desktop=true"

    next_page = "https://www.zhihu.com/api/v4/topics/19552747/feeds/essence?include=data%5B%3F%28target.type" \
                "%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content" \
                "%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type" \
                "%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal" \
                "%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type" \
                "%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type" \
                "%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count" \
                "%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type" \
                "%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count" \
                "%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics" \
                "%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author" \
                "%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type" \
                "%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cauthor.badge%5B%3F%28type" \
                "%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.comment_count&limit=10&offset={0}"

    more_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B*%5D.i' \
                      's_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_actio' \
                      'n%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_ed' \
                      'it%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2' \
                      'Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Crevie' \
                      'w_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2' \
                      'Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.mark_infos%5B*%5D.ur' \
                      'l%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.t' \
                      'opics&offset={1}&limit={2}&sort_by=default'



    def __init__(self):
        self.headers = HEADER
        self.cookies = COOKIES
        self.post_data = POST_DATA
        self.question_count = QUESTION_COUNT
        self.answer_count = ANSWER_COUNT_PER_QUESTION
        self.answer_offset = ANSWER_OFFSET

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield Request(url, meta={'cookiejar': i},
                              headers=self.headers,
                              cookies=self.cookies,
                              callback=self.login_success)  # jump to login page

    def login_zhihu(self, response):
        xsrf = re.findall(r'name="_xsrf" value="(.*?)"/>', response.text)[0]
        self.headers['X-Xsrftoken'] = xsrf
        self.post_data['_xsrf'] = xsrf

        times = re.findall(r'<script type="text/json" class="json-inline" data-n'
                           r'ame="ga_vars">{"user_created":0,"now":(\d+),', response.text)[0]
        captcha_url = 'https://www.zhihu.com/' + 'captcha.gif?r=' + times + '&type=login&lang=cn'

        yield Request(captcha_url, headers=self.headers, meta={'post_data': self.post_data},
                             callback=self.veri_captcha)

    def veri_captcha(self, response):
        with open('captcha.jpg', 'wb') as f:
            f.write(response.body)

        print('only one inverted number, 0')
        loca1 = input('input the loca 1:')
        loca2 = input('input the loca 2:')
        captcha = self.location(int(loca1), int(loca2))

        self.post_data = response.meta.get('post_data', {})
        self.post_data['captcha'] = captcha
        post_url = 'https://www.zhihu.com/login/email'

        yield FormRequest(post_url, formdata=self.post_data, headers=self.headers,
                                 callback=self.login_success)

    def location(self, a, b):
        if b != 0:
            captcha = "{\"img_size\":[200,44],\"input_points\":[%s,%s]}" % (str(self.capacha_index[a - 1]),
                                                                            str(self.capacha_index[b - 1]))
        else:
            captcha = "{\"img_size\":[200,44],\"input_points\":[%s]}" % str(self.capacha_index[a - 1])
        return captcha

    def login_success(self, response):
        yield Request('https://www.zhihu.com/topic/19552747/top-answers', headers=self.headers, dont_filter=True,
                          callback=self.parse_item, cookies=self.cookies)

    def parse_item(self, response):
        question_urls = re.findall(r'https://www.zhihu.com/question/(\d+)', response.text)

        # self.session_token = re.findall(r'session_token=([0-9,a-z]{32})', response.text)[0]

        for url in question_urls:
            question_detail = 'https://www.zhihu.com/question/' + url
            yield Request(question_detail, headers=self.headers, callback=self.parse_question)
            break

        n = 5
        while n < self.question_count:
            yield Request(self.next_page.format(n), headers=self.headers,
                          callback=self.get_more_question)
            n += 10

    def parse_question(self, response):
        # sel = Selector(response)
        item = ZhihuQuestionItem()
        text = response.text

        # xpath not familiar
        # item['name'] = sel.xpath('//h1[@class="QuestionHeader-title"]/text()').extract()
        # item['url'] = sel.xpath('//meta[@itemProp="url"]/text()')

        item['name'] = re.findall(r'<meta itemProp="name" content="(.*?)"', text)[0]
        item['url'] = re.findall(r'<meta itemProp="url" content="(.*?)"', text)[0]
        item['keywords'] = re.findall(r'<meta itemProp="keywords" content="(.*?)"', text)[0]
        item['answer_count'] = re.findall(r'<meta itemProp="answerCount" content="(.*?)"', text)[0]
        item['comment_count'] = re.findall(r'<meta itemProp="commentCount" content="(.*?)"', text)[0]
        item['flower_count'] = re.findall(r'<meta itemProp="zhihu:followerCount" content="(.*?)"', text)[0]
        item['date_created'] = re.findall(r'<meta itemProp="dateCreated" content="(.*?)"', text)[0]

        count_answer = int(item['answer_count'])
        yield item

        question_id = int(re.match(r'https://www.zhihu.com/question/(\d+)', response.url).group(1))

        if count_answer > self.answer_count:
            count_answer = self.answer_count
        n = self.answer_offset
        while n + 20 <= count_answer:
            yield Request(self.more_answer_url.format(question_id, n, n + 20), headers=self.headers,
                                 callback=self.parse_answer)
            n += 20

        yield Request(self.more_answer_url.format(question_id, n, count_answer), headers=self.headers,
                      callback=self.parse_answer)


    def get_more_question(self, response):
        question_url = 'http://www.zhihu.com/question/{0}'
        questions = json.loads(response.text)

        for que in questions['data']:
            target = que['target']
            if target.has_key('question'):
                question_id = re.findall(r'/(\d+)', target['question']['url'])[0]
                yield Request(question_url.format(question_id), headers=self.headers,
                                 callback=self.parse_question)

    def parse_answer(self, response):
        answers = json.loads(response.text)

        for ans in answers['data']:
            item = ZhihuAnswerItem()
            item['title'] = ans['question']['title']
            item['author'] = ans['author']['name']
            item['ans_url'] = ans['url']
            item['comment_count'] = ans['comment_count']
            item['upvote_count'] = ans['voteup_count']
            item['excerpt'] = ans['excerpt']
            yield item




