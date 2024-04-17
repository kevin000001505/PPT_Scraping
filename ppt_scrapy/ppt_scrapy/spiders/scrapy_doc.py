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
            title = row.xpath(".//div[@class='title']/a/text()").get()
            url = row.xpath(".//div[@class='title']/a/@href").get()
            match = re.search(r'\[(.*?)\]', title)
            yield {
                '列表名稱': match.group(1),
                '網址': url,
            }