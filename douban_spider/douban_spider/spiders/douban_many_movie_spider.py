from scrapy.spider import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from douban_spider.items import DoubanSpiderItem, DoubanBookItem

class DoubanSpider(Spider):

    name = "douban_spider"

    download_delay = 1

    allowed_domains = ["book.douban.com"]

    # start_urls=["https://movie.douban.com/people/116448906/collect?start=0&sort=time&rating=all&filter=all&mode=grid"]

    start_urls=["https://book.douban.com/tag/%E5%8E%86%E5%8F%B2?start=20&type=S"]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Referer': 'https://book.douban.com'
    }

    def start_requests(self):
        yield FormRequest("https://accounts.douban.com/login", headers=self.headers, formdata={"form_email": "xxxxxx",
        "form_password": "xxxxxxx"}, callback=self.logged_in)

    def logged_in(self, response):
        yield Request(url=self.start_urls[0], headers=self.headers, callback=self.parse)



    def parse(self, response):
        sel = Selector(response)
        item = DoubanBookItem()

        # movie_name = sel.xpath('//li[@class="title"]/a/em/text()').extract()
        book_name = sel.xpath('//div[@class="info"]/h2/a/./@title').extract()

        # star = sel.xpath('//li/span/@class').extract()
        # star = sel.xpath('//div[@class="info"]/div/div/span/@class').extract()
        star = sel.xpath('//div[@class="info"]/div/span[@class="rating_nums"]/text()').extract()

        # star = map(lambda b: b[6], filter(lambda a: a.startswith("rating"), star))


        # item['movie_name'] = [n.encode('utf-8') for n in movie_name]
        # item['star'] = [n.encode('utf-8') for  n in star]

        item['book_name'] = [n.encode('utf-8') for n in book_name]
        item['star'] = [n.encode('utf-8') for n in star]


        yield item

        next_page = sel.xpath('//span[@class="next"]/link/@href').extract()[0]
        next_full_page = response.urljoin(next_page)
        yield Request(next_full_page, headers=self.headers, callback=self.parse)

class DoubanSpider_2(Spider):
    new_request_url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start={0}"

    name = "douban_all_spider"

    download_delay = 1

    allowed_domains = ["movie.douban.com"]

    # start_urls=["https://movie.douban.com/people/116448906/collect?start=0&sort=time&rating=all&filter=all&mode=grid"]

    start_urls = ["https://movie.douban.com/tag/#/"]

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Referer': 'https://movie.douban.com'
    }

    def start_requests(self):
        yield FormRequest("https://accounts.douban.com/login", headers=self.headers, formdata={"form_email": "xxxxxx",
        "form_password": "xxxxxx"}, callback=self.logged_in)

    def logged_in(self, response):
        for i in range(10000):
            cur_url = self.new_request_url.format(i)


