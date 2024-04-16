# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PptScrapyItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    category = scrapy.Field()
class PptCommentScrapyItem(scrapy.Item):
    comment_author = scrapy.Field()
    comment_date = scrapy.Field()
    comment_content = scrapy.Field()

