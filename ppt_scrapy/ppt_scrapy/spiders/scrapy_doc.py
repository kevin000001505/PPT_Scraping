import scrapy
import re

class ScrapyDocSpider(scrapy.Spider):
    name = 'scrapy_doc'
    custom_settings = {
        'ITEM_PIPELINES': {
            'ppt_scrapy.pipelines.Task1Pipeline':300
        }
    }
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.parse)
    
    def parse(self, response):
        table = response.xpath("//div[@class='r-ent']")
        for row in table:
            link = row.xpath(".//div[@class='title']/a/@href").get()
            yield scrapy.Request(url=f'https://www.ptt.cc{link}', cookies={'over18': '1'}, callback=self.extract_board)
    
    def extract_board(self, response):
        url = response.url
        category = response.xpath("(//span[@class='article-meta-value'])[2]/text()").get()
        yield {
            '列表名稱': category,
            '列表網址': url,
        }

        