import json
import os
import time

import scrapy
from scrapy.http import Response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# __NUXT__.state.category.categories.children


class CategorySpider(scrapy.Spider):
    name = "category"

    cookies_path = os.path.join(os.path.dirname(__file__), "..", "cookies.json")
    with open(cookies_path, "r") as f:
        cookies = json.load(f)

    headers_path = os.path.join(os.path.dirname(__file__), "..", "headers.json")
    with open(headers_path, "r") as f:
        headers = json.load(f)

    def __init__(self):
        # change the user agent not to be detected as a bot
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
        )
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def start_requests(self):
        url = "https://zakupy.auchan.pl/shop/artykuly-spozywcze.c-11908"
        self.driver.get(url)
        time.sleep(3)

        self.driver.quit()

        body = str.encode(self.driver.page_source)

        # TODO: use middleware or not as a spider
        yield scrapy.Request(
            url,
            headers=self.headers,
            cookies=self.cookies,
            body=body,
            method="POST",
            callback=self.parse,
        )

    def parse(self, response: Response):
        a_selectors = response.xpath("//a")

        for a in a_selectors:
            # if '/shop/' in a.xpath("@href").get():
            url = a.xpath("@href").get()
            text = a.xpath("text()").get()
            if "/shop/" in url:
                print(url)
                yield {"url": url, "text": text}
