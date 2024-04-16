import scrapy


class ScrapyDocSpider(scrapy.Spider):
    name = 'scrapy_doc'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['http://www.ptt.cc/']

    def parse(self, response):
        pass
