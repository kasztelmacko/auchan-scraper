import os
import re
import sqlite3
import xml.etree.ElementTree as ET

import requests

url = "https://zakupy.auchan.pl/sitemap-categories.xml"

r = requests.get(url)

# load response into xml
xml = ET.fromstring(r.content)

# export all url to a list and then insert massivly to db

urls = []

regex_url = re.compile(
    r"^https:\/\/zakupy.auchan.pl\/shop\/([a-z\-\.]+)\/*([a-z\-\.]*)\/([a-z\-\.]+)\-(\d+)$"
)

regex_id = re.compile(
    r"^https:\/\/zakupy.auchan.pl\/shop\/[a-z\-\.]+\/*[a-z\-\.]*\/[a-z\-\.]+\-(\d+)$"
)

# https://zakupy.auchan.pl/shop/alkohole/cydr.c-27723

# "https://zakupy.auchan.pl/shop/zdrowa-zywnosc/pewni-dobrego/warzywa-owoce.c-24797"


for url in xml.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
    url = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
    match = regex_url.match(url)
    if match:
        print("match", url)
        result = re.findall(regex_url, url)[0]
        print(result)
        id = re.search(regex_id, url).group(1)
        cat_1 = result[0] if len(result) > 2 else None
        cat_2 = result[2] if result[1] == "" else result[1]
        product_name = result[2] if result[1] != "" else result[1]
        urls.append((id, url, cat_1, cat_2, product_name))
        print(id, url)
    else:
        print("no match", url)

current_path = os.path.dirname(os.path.realpath(__file__))
connection = sqlite3.connect(os.path.join(current_path, "auchan.db"))
curr = connection.cursor()

# insert all from urls to db
curr.executemany(
    "insert into category (id, url, cat_1, cat_2, product_name) values (?, ?, ?, ?, ?)",
    urls,
)

connection.commit()
