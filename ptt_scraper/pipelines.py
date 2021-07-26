# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from ptt_scraper import settings

class PttScraperPipeline:
    def __init__(self):
        self.db = sqlite3.connect(settings.DB_PATH)
        self.cursor = self.db.cursor()
        self.cursor.execute("DELETE FROM Post")
    def process_item(self, item, spider):
        query = f'INSERT INTO Post(title, push, author, comments) VALUES(\'{item["title"]}\''\
                f', {item["push"]}, \'{item["author"]}\', \'{item["comments"]}\')'
        try:
            
            self.cursor.execute(query)
        except:
            return
        
        
        return item
    def close_spider(self, spider):
        self.db.commit()
        self.db.close()
    