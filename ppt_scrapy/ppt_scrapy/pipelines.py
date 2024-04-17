# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os

class PptScrapyPipeline:
    def open_spider(self, spider):
        #self.file = open('PPT_post_comment.json', 'w')
        pass
    def close_spider(self, spider):
        #self.file.close()
        pass
    def process_item(self, item, spider):
        file_path = os.path.join('/Users/kevinhsu/Documents/GitHub/PPT_Scraping/ppt_scrapy/data', f"{item['title']}.json")
        with open(file_path, 'w', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False)
            file.write(line + "\n")
        return item
        #line = json.dumps(dict(item), ensure_ascii=False)
        #self.file.write(line + "\n")
        #return item

class Task1Pipeline:
    def open_spider(self, spider):
        self.file = open('task1_results.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item