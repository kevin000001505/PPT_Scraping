# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
import mysql.connector

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

class PPtMySQLPipeline:
    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@America155088',
            database='PPT'
        )
        self.cursor = self.connection.cursor()
    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
    
    def process_item(self, item, spider):
        comments = '/'.join([comment['comment_content'] for comment in item['post_comment']])

        contents = ' '.join(subitem for item in item.get('content') for subitem in (item if isinstance(item, list) else [item]))
        
        query = "INSERT INTO posts_details (title, author, date, content, comments, category) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            item.get('title'),
            item.get('author'),
            item.get('date'),
            contents,
            comments,
            item.get('category')
        )
        self.cursor.execute(query, values)
        self.connection.commit()
        return item