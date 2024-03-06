import json
import os

import scrapy

from auchan_scraper.itemloader import AuchanProductLoader
from auchan_scraper.items import AuchanItem


class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["auchan.pl"]
    cookies_path = os.path.join(os.path.dirname(__file__), "cookies.json")
    items_per_page = 15

    def start_requests(self):
        # read cookies from file

        with open(self.cookies_path, "r") as f:
            cookies = json.load(f)

        # headers to make the request
        headers = {
            "authority": "zakupy.auchan.pl",
            "accept": "application/json",
            "accept-language": "pl",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMWMyZWQ3N2QyYTQ3YWM4YTAxZDc4MDMwZWFhMWEyYyIsImp0aSI6IjBiYjE2OWE2MDZjZTRlZTM5Y2ZhY2QyZGRjMjYyOGU1ZTVlMDE4Nzk5NzBmYmI3MTdlMjhmNDkzY2ZmNmI2YjI1MjQ5MmRmYTE4YTE1MTE4IiwiaWF0IjoxNzA5NjU4MjkyLjcyMjU4NiwibmJmIjoxNzA5NjU4MjkyLjcyMjU5MSwiZXhwIjoxNzA5NzQ0NjkyLjcwMjIwOCwic3ViIjoiYW5vbl9mZmRlZmZiMC04NWUyLTQ3OTUtOTkyYi0yY2U5NDIzOTc3YTQiLCJzY29wZXMiOltdfQ.mg7yvagIJ3aLM_zCUtm3kCwghXJaf_uMSReIEnw3iRD3JEKNGgCRRf0iMF36NUHiDkQ5TU6fQmVHbcEBW-GFL2RkZZ_NR8BL7WF7gzDkRSaxTfFFhmP7hnX9zfZ5i9Chkv8LPXGLwfDoW0fFAr2XdFiQTL4CyTf3CLRbBqxkRN9lF0ajIJLN9Oy3y9EtYF3P_Rc12zE2bCEpD4xapfCLWdE4Uv1y8pVPFx4EyG3Zi7mSlMBRW6aPZr4QA5NsookBBa2NO9qw6db91vLwcRQo0uN4kHIOuiCgd1kXMUb2J_V6-fpWscu5zcOoj6FT-jp0nAF6NbhWp79siqdTVy19TQ",
            "cookie": "userIsLoggedIn=false; OptanonAlertBoxClosed=2024-02-29T17:07:33.908Z; _gcl_au=1.1.376956713.1709226454; _ga=GA1.1.1356565571.1709226451; startup_popup_closed=true; FPID=FPID2.2.uF21TJcFOW0iNFvUltA%2BLjcjh2z24anV0yv4jpCIybY%3D.1709226451; FPAU=1.1.376956713.1709226454; token_type=Bearer; access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMWMyZWQ3N2QyYTQ3YWM4YTAxZDc4MDMwZWFhMWEyYyIsImp0aSI6ImQwMDI3ZDFhZGM2OTE5YzUzOGIzNjU0MzViNDEyZGJhMmQ1YzYxNTI5MzkzMDBjOTU4YzM3YTM5NDYxNWUwOGFjZDcwMDIxNjk5ZjQ5MGZkIiwiaWF0IjoxNzA5NDY1NzM2LjA2ODk2LCJuYmYiOjE3MDk0NjU3MzYuMDY4OTY3LCJleHAiOjE3MDk1NTIxMzYuMDQzMDQzLCJzdWIiOiJhbm9uXzI2NWEwYjI5LTE0ZTQtNGU4Zi04MjdlLWQ0Y2NlYzM0ODdlOSIsInNjb3BlcyI6W119.gAyghmif5z1p7x0oGtLHE9WXlZOVUHlbsXF3i2Lcr_tIwPH3mZ5UrpsYetTITmsME7WsVJZzZ6Zv0UySMylFYWkjK949JvKOKtCQgEgREJ_oPYIh79JiP5BxA0MtBSmYwniawHcpZg1FuUtSSXs4NSwkDduiloIEGdHIA9NpA0GCrJDI81wlzAG1mFuEjJxHGZBZXlJy1KDHXvtMVVRqDKF_xbq4V6eCrNsO6hdN1DIa0MJ-sn_5eBDxqXrrz2_fiUEHMM12Ccbs9oKecuPxm3lzJ8tOw3wfo0cLybfspsfvCW8rBPKMDNjzg3g1sKy9KVOgcqLKspB8VP8kfH3coQ; refresh_token=def5020098cd87384253d6454669965d073b2133a44505b483950f05c29d388c52729342213bd2cb674f992cc17c98d1dd1a88e56d4acdc05b49c46619910f2892db977d7934c99915a116555e2a45c2c8412e950ddc4c5fd77af49433ecd1f15ff49c5c9b50dcdb48a58b81c8505a877683b681608eaafffd1332a838902220b7c979f728db17dbfb944e722772592304021f006f98e03ca4bf76858378129549efbc849fac686e1c7d9f1be5aa39a9e8dd72262eaf63b9053976541d94040a69a816f33c079cb198bd659ffd017e40d27ee35a73b8979be0cb80d2c0e895a81df1bc8028ecfbdc95828be1890578d4016c879d3b688c8f7b039b76f48f1f40d3e5f756267549f6b09a12d4d86cab450f6ba66de1e3e68be49a5dee24fd87076b48a005a82f97bb22df295fa66827a94ea269801fedad7837778b072761b3afddac91f57027521796ba7debec9e54cf27615740ba6c0d21648643ed372012efe3461128c47e41cb1b7bf08d457708c7ce2b6d18b97f31a726f4f10a45bf6fc8025a5018dc0d9d602fe8236386f4428e08c3999b318413357328b2c5bbe92d9e6a8de4b85eb8711466f4; _uetsid=27aefa60d95211eeb6e49df2961961ef; _uetvid=062c3da0d72511ee908eaba7439d8c47; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Mar+03+2024+12%3A35%3A37+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=202211.2.0&isIABGlobal=false&consentId=ced87ba0-6136-4132-a31c-54673cbc9d61&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0007%3A1&hosts=H216%3A1%2CH56%3A1%2CH57%3A1%2CH58%3A1%2CH178%3A1%2CH179%3A1%2CH3%3A1%2CH4%3A1%2CH12%3A1%2CH235%3A1%2CH260%3A1%2CH335%3A1%2CH59%3A1%2CH326%3A1%2CH247%3A1&genVendors=V9%3A1%2CV16%3A1%2CV5%3A1%2CV15%3A1%2CV6%3A1%2CV10%3A1%2CV8%3A1%2CV33%3A1%2CV26%3A1%2CV4%3A1%2CV7%3A1%2C&geolocation=PL%3B14&AwaitingReconsent=false; _gcl_aw=GCL.1709465737.CjwKCAiA3JCvBhA8EiwA4kujZmiWcISuHairMRUEkAs2apS7WU-AoIt2F_LyOjkhD7M7PUMFX1T8XxoCGoIQAvD_BwE; _clck=z0ahc4%7C2%7Cfjr%7C0%7C1520; PHPSESSID=mmntjimkotpsfv5pnmjspk0907; FPGCLAW=GCL.1709465742.CjwKCAiA3JCvBhA8EiwA4kujZmiWcISuHairMRUEkAs2apS7WU-AoIt2F_LyOjkhD7M7PUMFX1T8XxoCGoIQAvD_BwE; FPLC=C7baqelxu58qZgQP89FCyd77k%2FOATm4Eqkie1hydAV%2FntjNVyM%2BBY7I6MGwEvz6MIX4zknkCWxv0CtNhWjjnb72HSZdR6WWg%2BsylgLSsAIgQJHlKI5wuDEuvVjNCZA%3D%3D; _clsk=15hm331%7C1709465745293%7C2%7C1%7Cx.clarity.ms%2Fcollect; _ga_12345=GS1.1.1709465737.8.1.1709465754.0.0.0; _ga_88WZ9X400Y=GS1.1.1709465737.8.1.1709465754.43.0.0; _ga_HFH1FZ6EXG=GS1.1.1709465737.8.1.1709465754.43.0.0; __utmz_gtm=utmcsr=google%7Cutmccn=(none)%7Cutmcmd=organic",
            "referer": "https://zakupy.auchan.pl/shop/artykuly-spozywcze/mleko-nabial-jaja/maslo-margaryny-tluszcze.c-28821",
            "sec-ch-ua": '^\^"Not A(Brand^\^";v=^\^"99^\^", ^\^"Opera^\^";v=^\^"107^\^", ^\^"Chromium^\^";v=^\^"121^\^"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '^\^"Android^\^"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
        }

        url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId=28821&itemsPerPage={self.items_per_page}&page=1&cacheSegmentationCode=019_DEF&hl=pl"
        yield scrapy.Request(url, cookies=cookies, headers=headers, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        page_count = data["pageCount"]  # get the number of pages for the category

        # get cookies and headers from the response
        cookies = response.request.cookies
        headers = response.request.headers

        # generate start_urls and make requests
        for i in range(2, page_count + 1):
            url = f"https://zakupy.auchan.pl/api/v2/cache/products?categoryId=28821&itemsPerPage={self.items_per_page}&page={i}&cacheSegmentationCode=019_DEF&hl=pl"
            yield scrapy.Request(
                url, cookies=cookies, headers=headers, callback=self.parse_products
            )

    def parse_products(self, response):
        data = json.loads(response.body)
        for product in data["results"]:
            loader = AuchanProductLoader(item=AuchanItem(), selector=product)
            loader.add_value("name", product["defaultVariant"]["name"])
            loader.add_value("category_name", product["categoryName"])
            loader.add_value("price", product["defaultVariant"]["price"]["gross"])
            loader.add_value("volume", product["defaultVariant"]["itemVolumeInfo"])
            yield loader.load_item()
