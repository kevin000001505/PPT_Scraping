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
        self.page = 1
        self.seven_days_ago = self.today - timedelta(days=7)

        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'over18': '1'}, callback=self.parse)

    def parse(self, response):
        document_item = PptScrapyItem()

        if self.page == 1:
            exclude_table = response.xpath("//div[@class='r-list-sep']/following-sibling::node()//div[@class='title']")
            exclude_list = []
            for exclude in exclude_table:
                exclude_list.append(exclude.xpath(".//a/@href").get())

        table = response.xpath("//div[@class='r-ent']")
        for row in table:
            title = row.xpath(".//div[@class='title']/a/text()").get()
            if title == None:
                continue
            link = row.xpath(".//div[@class='title']/a/@href").get()
            
            if self.page == 1 and link in exclude_list:
                continue

            check_date = row.xpath(".//div[@class='date']/text()").get().replace(' ', '')
            check_date = datetime.strptime(f"{check_date}/2024", '%m/%d/%Y').date()
            if self.today <= check_date: # using today for test 
                
                date = row.xpath(".//div[@class='date']/text()").get()
                document_item['simple_date'] = date
                
                match = re.search(r'\[(.*?)\]', title)
                if match != None:
                    category = match.group(1)
                else:
                    category = 'None'

                
                document_item['title'] = title
                document_item['category'] = category

                yield scrapy.Request(url=f'https://www.ptt.cc{link}', cookies={'over18': '1'}, callback=self.extract_comment, meta={'item': document_item})
            else:
                return 'Finished'
        print(title)
        time.sleep(2)
        last_page_link = response.xpath("//a[@class='btn wide'][2]/@href").get()

        self.page = 2
        yield scrapy.Request(url=f'https://www.ptt.cc{last_page_link}', cookies={'over18': '1'}, callback=self.parse)

    def extract_comment(self, response):
        document_item = response.meta.get('item')
        comments_item = PptCommentScrapyItem()

        num = 1
        content = []
        if '引述' in response.xpath("//div[@id='main-content']/span[1]/text()").get():
            further_content = []
            further_num = 1
            while '發信站' not in response.xpath(f"(//div[@id='main-content']/span/text())[{further_num}]").get():
                word = response.xpath(f"(//div[@id='main-content']/span/text())[{further_num}]").get().replace('\n', '').strip()
                further_content.append(word)
                further_num += 1
                if response.xpath(f"(//div[@id='main-content']/span/text())[{further_num}]").get() is None:
                    further_num += 1
            content.append(further_content)


        author = response.xpath("//div[@id='main-content']/div[1]/span[2]/text()").get()
        date = response.xpath("//div[@id='main-content']/div[4]/span[2]/text()").get()
        contents = response.xpath("//div[@id='main-content']/text()")
        while response.xpath(f"//div[@id='main-content']/text()[{num}]"):
            content.append(response.xpath(f"//div[@id='main-content']/text()[{num}]").get().replace('\n', '').strip())
            num += 1
        filter_content = [items for items in content if items != '']

        document_item['author'] = author
        document_item['explicity_date'] = date
        document_item['content'] = filter_content
        document_item['post_comment'] = []

        # Now deal with the comments
        comment_title = response.xpath("//div[@id='main-content']/div[3]/span[2]/text()").get()
        comments_table = response.xpath("//div[@class='push']")
        for comment in comments_table:
            comment_author = comment.xpath(".//span[@class='f3 hl push-userid']/text()").get()
            comment_content = comment.xpath(".//span[@class='f3 push-content']/text()[1]").get()
            comment_date = comment.xpath(".//span[@class='push-ipdatetime']/text()").get().replace('\n', '').split(' ')[-2::]

            comments_item['comment_author'] = comment_author
            comments_item['comment_date'] = comment_date
            comments_item['comment_content'] = comment_content.replace(': ', '')
            document_item['post_comment'].append(dict(comments_item))
        yield document_item

  



