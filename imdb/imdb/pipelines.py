# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import sqlite3


class MongodbPipeline:
    collection_name = "best_movies"
        
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("")
        self.db = self.client["IMDB"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(ItemAdapter(item).asdict())
        return item


class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("imdb.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE best_moives(
                    title TEXT,
                    year TEXT,
                    duration TEXT,
                    genre TEXT,
                    rating TEXT,
                    movie_url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
        
    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.c.execute('''
                SELECT title FROM imdb where title=?
            ''', (item['title']))
        except sqlite3.OperationalError:
            # First time running, does not have data
            pass
 
        result = self.c.fetchone()
        if result:
            # Already exists
            pass
        else:
            # Doesn't exists
            self.c.execute('''
            INSERT INTO best_moives (title, year, duration, genre, rating, movie_url) VALUES(?,?,?,?,?,?)
        ''', (
            item.get('title'),
            item.get('year'),
            item.get('duration'),
            item.get('genre'),
            item.get('rating'),
            item.get('movie_url')
        ))
            self.connection.commit()
        return item