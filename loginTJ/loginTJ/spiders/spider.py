import logging
import re
import sys
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, FormRequest, HtmlResponse
from scrapy.http.cookies import CookieJar

cookie_jar = CookieJar()


class TongJiSpider(CrawlSpider):
    post_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
        "Referer": "http://xuanke.tongji.edu.cn/index.jsp?flag=5",
    }

    name = "loginTJ"
    start_urls=["http://xuanke.tongji.edu.cn/index.jsp?flag=5"]

    rules = []

    def start_requests(self):
        yield FormRequest("https://ids.tongji.edu.cn:8443/nidp/saml2/sso?id=527&sid=1&option=credential&sid=1",
                          headers=self.post_headers, meta={"cookiejar": 1},
                          callback=self.logged_in, formdata={"Ecom_User_ID": "1452311", "Ecom_Password": "214231"},
                          )


    def logged_in(self, response):
        print response.text
        # cookies = {"JSESSIONID": "DBB390B986649B044FA46794F19DECBE.62"}
        yield Request("http://4m3.tongji.edu.cn/eams/home.action", headers=self.post_headers,
                      callback=self.parse)

    def parse(self, response):
        print response.text

