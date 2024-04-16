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
        table = response.xpath("//div[@class='r-ent']")
        for row in table:
            url = row.xpath(".//div[@class='title']/a/@href").get()
        yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.extract_comment)

    def extract_comment(self, response):
        document_item = PptScrapyItem()
        title = response.xpath("//div[@id='main-content']/div[3]/span[2]/text()").get()
        author = response.xpath("//div[@id='main-content']/div[1]/span[2]/text()").get()
        match = re.search(r'\[(.*?)\]', title)
        category = match.group(1)
        date = response.xpath("//div[@id='main-content']/div[4]/span[2]/text()").get()
        # Now deal with the comments

