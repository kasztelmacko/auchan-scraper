import scrapy
from auchan_scraper.items import AuchanItem
from auchan_scraper.itemloader import AuchanProductLoader
import json
import os

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["auchan.pl"]
    
    cookies_path = os.path.join(os.path.dirname(__file__), "cookies.json")
    with open(cookies_path, "r") as f:
            cookies = json.load(f)

    headers_path = os.path.join(os.path.dirname(__file__), "headers.json")
    with open(headers_path, "r") as f:
            headers = json.load(f)

    def start_requests(self):
        url = "https://zakupy.auchan.pl/api/v2/cache/products?categoryId=28821&itemsPerPage=15&page=1&cacheSegmentationCode=019_DEF&hl=pl"
        yield scrapy.Request(url, cookies=self.cookies, headers=self.headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        page_count = data['pageCount'] # get the number of pages for the category

        # generate start_urls and make requests
        for i in range(2, page_count + 1):
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId=28821&itemsPerPage=15&page={i}&cacheSegmentationCode=019_DEF&hl=pl"
            yield scrapy.Request(url, cookies=self.cookies, headers=self.headers, callback=self.parse_products)

    def parse_products(self, response):
        data = json.loads(response.body)
        for product in data['results']:
            loader = AuchanProductLoader(item=AuchanItem(), selector=product)
            loader.add_value('name', product["defaultVariant"]['name'])
            loader.add_value('category_name', product['categoryName'])
            loader.add_value('price', product["defaultVariant"]['price']['gross'])
            loader.add_value('volume', product["defaultVariant"]["itemVolumeInfo"])
            yield loader.load_item()
        