# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class AuchanPipeline:
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline:
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter["name"] in self.names_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.names_seen.add(adapter["name"])
            return item


class SavingTosqlitePipeline(object):
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        try:
            current_path = os.path.dirname(os.path.realpath(__file__))
            self.connection = sqlite3.connect(os.path.join(current_path, "auchan.db"))
            self.curr = self.connection.cursor()
            print("Połączono z bazą danych")
        except sqlite3.Error as e:
            print(f"Błąd połączenia z bazą danych: {e}")
        return self.connection

    def process_item(self, item, spider):
        print("Processing item in SavingTosqlitePipeline")
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute(
            """ insert into auchan (product_name, category_name, price, volume) values (?, ?, ?, ?)""",
            (item["name"], item["category_name"], item["price"], item["volume"]),
        )
        self.connection.commit()
        return self.curr
