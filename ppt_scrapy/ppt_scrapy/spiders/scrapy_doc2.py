import scrapy
import re
from ppt_scrapy.items import PptScrapyItem, PptCommentScrapyItem
import time
import datetime as dt
from datetime import datetime, timedelta

class ScrapyDocSpider(scrapy.Spider):
    name = 'scrapy_doc2'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']

    def start_requests(self):
        self.today = dt.date.today()
        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.parse)
    
    def parse(self, response):
        table = response.xpath("//div[@class='r-ent']")
        document_item = PptScrapyItem()
        for row in table:
            check_date = row.xpath(".//div[@class='date']/text()").get().replace(' ', '')
            check_date = datetime.strptime(f"{check_date}/2024", '%m/%d/%Y').date()
            seven_days_ago = self.today - timedelta(days=7)

            if seven_days_ago <= check_date <= self.today: # check date

                date = row.xpath(".//div[@class='date']/text()").get()
                link = row.xpath(".//div[@class='title']/a/@href").get()
                title = row.xpath(".//div[@class='title']/a/text()").get()
                author = row.xpath(".//div[@class='author']/text()").get()

                match = re.search(r'\[(.*?)\]', title)
                category = match.group(1)

                document_item['author'] = author
                document_item['title'] = title
                document_item['category'] = category
                yield scrapy.Request(url=f'https://www.ptt.cc{link}', cookies={'over18': '1'}, callback=self.extract_comment, meta={'item': document_item})
        
        last_page_link = response.xpath("//a[@class='btn wide'][2]/@href").get()
        yield response.follow(url=f'https://www.ptt.cc{last_page_link}', cookies={'over18': '1'}, callback=self.parse)


    def extract_comment(self, response):
        document_item = response.meta.get('item')
        comments_item = PptCommentScrapyItem()

        num = 1
        content = []

        date = response.xpath("//div[@id='main-content']/div[4]/span[2]/text()").get()
        contents = response.xpath("//div[@id='main-content']/text()")
        while response.xpath(f"//div[@id='main-content']/text()[{num}]"):
            content.append(response.xpath(f"//div[@id='main-content']/text()[{num}]").get().replace('\n', '').strip())
            num += 1
        filter_content = [items for items in content if items != '']

        document_item['date'] = date
        document_item['content'] = filter_content
        
        yield document_item

        # Now deal with the comments
        comments_table = response.xpath("//div[@class='push']")
        for comment in comments_table:
            comment_author = comment.xpath(".//span[@class='f3 hl push-userid']/text()").get()
            comment_content = comment.xpath(".//span[@class='f3 push-content']/text()[1]").get()
            comment_date = comment.xpath(".//span[@class='push-ipdatetime']/text()").get().replace('\n', '').split(' ')[-2::]

            comments_item['comment_author'] = comment_author
            comments_item['comment_date'] = comment_date
            comments_item['comment_content'] = comment_content
            yield comments_item

