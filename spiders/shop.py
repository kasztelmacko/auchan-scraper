import scrapy
from auchan_scraper.items import AuchanItem
from auchan_scraper.itemloader import AuchanProductLoader
import json
from auchan_scraper.utils import cookies, headers

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["auchan.pl"]

    def start_requests(self):
        url = "https://zakupy.auchan.pl/api/v2/cache/products?categoryId=28821&itemsPerPage=15&page=1&cacheSegmentationCode=019_DEF&hl=pl"
        yield scrapy.Request(url, cookies=cookies, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        page_count = data['pageCount'] # get the number of pages for the category

        # generate start_urls and make requests
        for i in range(2, page_count + 1):
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId=28821&itemsPerPage=15&page={i}&cacheSegmentationCode=019_DEF&hl=pl"
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
        