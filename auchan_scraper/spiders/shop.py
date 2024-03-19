import json
import os

import scrapy

from auchan_scraper.itemloader import AuchanProductLoader
from auchan_scraper.items import AuchanItem



class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["auchan.pl"]

    cookies_path = os.path.join(os.path.dirname(__file__), "..", "cookies.json")
    with open(cookies_path, "r") as f:
        cookies = json.load(f)

    headers_path = os.path.join(os.path.dirname(__file__), "..", "headers.json")
    with open(headers_path, "r") as f:
        headers = json.load(f)
    
    params_path = os.path.join(os.path.dirname(__file__), "..", "params.json")
    with open(params_path, "r") as f:
        params = json.load(f)

    start_url = params.get('start_url')
    category_id = params.get('category_id')

    def start_requests(self):
        if self.start_url is not None:
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId={self.category_id}&itemsPerPage=15&page=1&cacheSegmentationCode=019_DEF&hl=pl"
            yield scrapy.Request(
                url, cookies=self.cookies, headers=self.headers, callback=self.parse
            )

    def parse(self, response):
        data = json.loads(response.body)
        page_count = data["pageCount"]  # get the number of pages for the category

        # Loop over the products on the current page
        for product in data["results"]:
            loader = AuchanProductLoader(item=AuchanItem(), selector=product)
            fields = {
                "name": product.get("defaultVariant", {}).get("name", "Unknown"),
                "category_name": product.get("categoryName", "Unknown"),
                "price": product.get("defaultVariant", {}).get("price", {}).get("gross", "Unknown"),
                "currency": product.get("defaultVariant", {}).get("price", {}).get("currency", "Unknown"),
                "volume": product.get("defaultVariant", {}).get("itemVolumeInfo", "Unknown"),
                "unit": product.get("defaultVariant", {}).get("itemVolumeInfo", "Unknown"),
            }
            for field, value in fields.items():
                loader.add_value(field, value)
            yield loader.load_item()

        # Generate start_urls and make requests for subsequent pages
        for i in range(2, page_count + 1):
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId={self.category_id}&itemsPerPage=15&page={i}&cacheSegmentationCode=019_DEF&hl=pl"
            yield scrapy.Request(
                url,
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse,
        )
