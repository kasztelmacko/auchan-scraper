import scrapy
import json
import re
from auchan_scraper.items import AuchanItem
from auchan_scraper.itemloader import AuchanProductLoader
from auchan_scraper.utils import cookies, headers

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["auchan.pl"]

    def start_requests(self):
        url = "https://zakupy.auchan.pl/lp-najtaniej-w-auchan"
        yield scrapy.Request(url, cookies=cookies, headers=headers, callback=self.parse_categories)

    def parse_categories(self, response):
        category_ids = response.css('*::text').re(r'\b\d{5}\b')
        category_ids = list(map(int, category_ids))
        for category_id in category_ids:
            yield from self.create_requests(category_id)

    def create_requests(self, category_id):
        url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId={category_id}&itemsPerPage=15&page=1&cacheSegmentationCode=019_DEF&hl=pl"
        yield scrapy.Request(url, cookies=cookies, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        page_count = data['pageCount'] # get the number of pages for the category

        # get category_id from the URL
        category_id = re.search(r'categoryId=(\d+)', response.url).group(1)

        # generate start_urls and make requests
        for i in range(2, page_count + 1):
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId={category_id}&itemsPerPage=15&page={i}&cacheSegmentationCode=019_DEF&hl=pl"
            yield scrapy.Request(url, cookies=cookies, headers=headers, callback=self.parse_products)

    def parse_products(self, response):
        data = json.loads(response.body)
        for product in data['results']:
            loader = AuchanProductLoader(item=AuchanItem(), selector=product)
            loader.add_value('name', product["defaultVariant"]['name'])
            loader.add_value('category_name', product['categoryName'])
            loader.add_value('price', product["defaultVariant"]['price']['gross'])
            loader.add_value('volume', product["defaultVariant"]["itemVolumeInfo"])
            yield loader.load_item()
        