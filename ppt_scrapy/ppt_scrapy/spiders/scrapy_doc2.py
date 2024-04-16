import scrapy
import re
from ppt_scrapy.items import PptScrapyItem, ComentScrapyItem

class ScrapyDocSpider(scrapy.Spider):
    name = 'scrapy_doc'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.parse)
    
    def parse(self, response):
        document_item = PptScrapyItem()
        table = response.xpath("//div[@class='r-ent']")
        for row in table:
            # 標題
            document_item['title'] = row.xpath(".//div[@class='title']/a/text()").get()
            url = row.xpath(".//div[@class='title']/a/@href").get()
            match = re.search(r'\[(.*?)\]', title)
            # 累別
            document_item['category'] = match.group(1)
            # 作者
            document_item['author'] = row.xpath(".//div[@class='author']/text()").get()
            # 發布時間
            document_item['date'] = row.xpath(".//div[@class='date']/text()").get()

        yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.extract_comment)
    def extract_comment(self, response):
        # remember content
        pass