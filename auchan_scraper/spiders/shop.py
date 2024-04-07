import json
import logging
import os
import random

import scrapy

from auchan_scraper.itemloader import AuchanProductLoader
from auchan_scraper.items import AuchanItem

DEFAULT_VALUE = "Unknown"


def get_categories() -> list[(str, str)]:
    categories_path = os.path.join(os.path.dirname(__file__), "..", "categories.json")
    with open(categories_path, "r") as f:
        categories = json.load(f)
        subcategories = [
            (subcategory["url"], subcategory["url"].split("c-")[-1])
            for category in categories
            for subcategory in category["subcategories"]
        ]
    return subcategories


def get_headers(cookies: dict) -> dict[str, str]:
    headers = {
        "authority": "zakupy.auchan.pl",
        "accept": "application/json",
        "accept-language": "pl",
        "sec-ch-ua": '^\^"Not A(Brand^\^";v=^\^"99^\^", ^\^"Opera^\^";v=^\^"107^\^", ^\^"Chromium^\^";v=^\^"121^\^"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '^\^"Android^\^"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    }

    if cookies:
        headers["Cookie"] = "; ".join(
            [f"{cookie['name']}={cookie['value']}" for cookie in cookies]
        )

        auth_token = next(
            (cookie["value"] for cookie in cookies if cookie["name"] == "access_token"),
            None,
        )
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

    return headers


class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["auchan.pl"]

    cookies_path = os.path.join(os.path.dirname(__file__), "..", "cookies.json")
    with open(cookies_path, "r") as f:
        cookies = json.load(f)

    headers = get_headers(cookies)

    def __init__(self, number, *args, **kwargs):
        super(ShopSpider, self).__init__(*args, **kwargs)
        self.number = int(number)

    def start_requests(self):
        subcategories = get_categories()
        subcategories = random.sample(subcategories, self.number)

        for subcategory_url, category_id in subcategories:
            self.headers["referer"] = subcategory_url
            print(category_id, subcategory_url)
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId={category_id}&itemsPerPage=15&page=1&cacheSegmentationCode=019_DEF&hl=pl"
            yield scrapy.Request(
                url=url, cookies=self.cookies, headers=self.headers, callback=self.parse
            )

    def parse(self, response):
        data = json.loads(response.body)
        page_count = data["pageCount"]  # get the number of pages for the category
        print(response.url)
        category_id = response.url.split("categoryId=")[-1].split("&")[0]

        # Loop over the products on the current page
        for product in data["results"]:
            loader = AuchanProductLoader(item=AuchanItem(), selector=product)
            fields = {
                "name": product.get("defaultVariant", {}).get("name", DEFAULT_VALUE),
                "category_name": product.get("categoryName", DEFAULT_VALUE),
                "price": product.get("defaultVariant", {})
                .get("price", {})
                .get("gross", DEFAULT_VALUE),
                "currency": product.get("defaultVariant", {})
                .get("price", {})
                .get("currency", DEFAULT_VALUE),
                "volume": product.get("defaultVariant", {}).get(
                    "itemVolumeInfo", DEFAULT_VALUE
                ),
                "unit": product.get("defaultVariant", {}).get(
                    "itemVolumeInfo", DEFAULT_VALUE
                ),
                "volume_info": product.get("defaultVariant", {}).get(
                    "itemVolumeInfo", DEFAULT_VALUE
                ),
                "package_unit": product.get("defaultVariant", {})
                .get("packageInfo", {})
                .get("packageUnit", DEFAULT_VALUE),
                "package_size": product.get("defaultVariant", {})
                .get("packageInfo", {})
                .get("packageSize", DEFAULT_VALUE),
            }

            logging.debug(str(fields))

            for field, value in fields.items():
                loader.add_value(field, value)
            yield loader.load_item()

        # Generate start_urls and make requests for subsequent pages
        for i in range(2, page_count + 1):
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId={category_id}&itemsPerPage=15&page={i}&cacheSegmentationCode=019_DEF&hl=pl"
            yield scrapy.Request(
                url,
                cookies=self.cookies,
                headers=self.headers,
                callback=self.parse,
            )
