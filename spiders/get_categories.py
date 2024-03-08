import scrapy
import re
from auchan_scraper.utils import cookies, headers

class GetCategoriesSpider(scrapy.Spider):
    name = "get_categories"
    allowed_domains = ["auchan.pl"]

    def start_requests(self):
        url = "https://zakupy.auchan.pl/lp-najtaniej-w-auchan"
        yield scrapy.Request(url, cookies=cookies, headers=headers, callback=self.parse)

    def parse(self, response):
        category_ids = response.css('*::text').re(r'\b\d{5}\b')
        category_ids = list(map(int, category_ids))
        
        with open('category_ids.txt', 'w') as f:
            for id in category_ids:
                f.write(f'{id}\n')
    
        