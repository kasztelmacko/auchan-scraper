import json
import re
import time
from datetime import date, datetime
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url = input("Enter the URL of the website: ")

parsed_url = urlparse(url)

if parsed_url.netloc == "zakupy.auchan.pl" and parsed_url.path.startswith("/shop"):
    last_six_chars = url[-5:]
    if last_six_chars.isdigit():
        category_id = last_six_chars
    else:
        category_id = None

    # Save the URL and category ID in a JSON file
    params = {"start_url": url, "category_id": category_id}
    with open("params.json", "w") as f:
        json.dump(params, f)
else:
    raise ValueError(
        "Invalid URL. The URL must be from the domain 'https://zakupy.auchan.pl/shop'"
    )


# change the user agent not to be detected as a bot
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
)
options.add_argument("--ignore-certificate-errors")
driver = webdriver.Chrome(options=options)

# open the website and wait for cookies to load
driver.get(url)
time.sleep(3)


# accept cookies popup
action_1 = ActionChains(driver)
element = driver.find_element(By.ID, "onetrust-accept-btn-handler")
action_1.move_to_element(element).click().perform()
now = datetime.now()
time.sleep(4)

# accept advertisement popup
action_2 = ActionChains(driver)
element = driver.find_element(By.XPATH, "//*[@aria-label='Zamknij okno dialogowe']")
action_2.move_to_element(element).click().perform()

# get cookies when the full website is loaded
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for the page to load

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # If heights are the same it means end of scrolling
        break
    last_height = new_height

cookies = driver.get_cookies()

response = requests.get(url)
headers = response.headers
access_token = headers["Set-Cookie"]
match = re.search(r"access_token=(.*?);", access_token)
if match:
    access_token = "Bearer " + match.group(1)
headers = {
    "authority": "zakupy.auchan.pl",
    "accept": "application/json",
    "accept-language": "pl",
    "authorization": access_token,
    "cookie": f"userIsLoggedIn=false; OptanonAlertBoxClosed={date.today()}T{now.strftime('%H:%M:%S')}.908Z; _gcl_au=1.1.376956713.1709226454; _ga=GA1.1.1356565571.1709226451; startup_popup_closed=true; FPID=FPID2.2.uF21TJcFOW0iNFvUltA%2BLjcjh2z24anV0yv4jpCIybY%3D.1709226451; FPAU=1.1.376956713.1709226454; token_type=Bearer; access_token={access_token}; refresh_token=def5020098cd87384253d6454669965d073b2133a44505b483950f05c29d388c52729342213bd2cb674f992cc17c98d1dd1a88e56d4acdc05b49c46619910f2892db977d7934c99915a116555e2a45c2c8412e950ddc4c5fd77af49433ecd1f15ff49c5c9b50dcdb48a58b81c8505a877683b681608eaafffd1332a838902220b7c979f728db17dbfb944e722772592304021f006f98e03ca4bf76858378129549efbc849fac686e1c7d9f1be5aa39a9e8dd72262eaf63b9053976541d94040a69a816f33c079cb198bd659ffd017e40d27ee35a73b8979be0cb80d2c0e895a81df1bc8028ecfbdc95828be1890578d4016c879d3b688c8f7b039b76f48f1f40d3e5f756267549f6b09a12d4d86cab450f6ba66de1e3e68be49a5dee24fd87076b48a005a82f97bb22df295fa66827a94ea269801fedad7837778b072761b3afddac91f57027521796ba7debec9e54cf27615740ba6c0d21648643ed372012efe3461128c47e41cb1b7bf08d457708c7ce2b6d18b97f31a726f4f10a45bf6fc8025a5018dc0d9d602fe8236386f4428e08c3999b318413357328b2c5bbe92d9e6a8de4b85eb8711466f4; _uetsid=27aefa60d95211eeb6e49df2961961ef; _uetvid=062c3da0d72511ee908eaba7439d8c47; OptanonConsent=isGpcEnabled=0&datestamp={now.strftime('%a+%b+%d+%Y')}+12%3A35%3A37+GMT%2B0100+(czas+%C5%9Brodkowoeuropejski+standardowy)&version=202211.2.0&isIABGlobal=false&consentId=ced87ba0-6136-4132-a31c-54673cbc9d61&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0007%3A1&hosts=H216%3A1%2CH56%3A1%2CH57%3A1%2CH58%3A1%2CH178%3A1%2CH179%3A1%2CH3%3A1%2CH4%3A1%2CH12%3A1%2CH235%3A1%2CH260%3A1%2CH335%3A1%2CH59%3A1%2CH326%3A1%2CH247%3A1&genVendors=V9%3A1%2CV16%3A1%2CV5%3A1%2CV15%3A1%2CV6%3A1%2CV10%3A1%2CV8%3A1%2CV33%3A1%2CV26%3A1%2CV4%3A1%2CV7%3A1%2C&geolocation=PL%3B14&AwaitingReconsent=false; _gcl_aw=GCL.1709465737.CjwKCAiA3JCvBhA8EiwA4kujZmiWcISuHairMRUEkAs2apS7WU-AoIt2F_LyOjkhD7M7PUMFX1T8XxoCGoIQAvD_BwE; _clck=z0ahc4%7C2%7Cfjr%7C0%7C1520; PHPSESSID=mmntjimkotpsfv5pnmjspk0907; FPGCLAW=GCL.1709465742.CjwKCAiA3JCvBhA8EiwA4kujZmiWcISuHairMRUEkAs2apS7WU-AoIt2F_LyOjkhD7M7PUMFX1T8XxoCGoIQAvD_BwE; FPLC=C7baqelxu58qZgQP89FCyd77k%2FOATm4Eqkie1hydAV%2FntjNVyM%2BBY7I6MGwEvz6MIX4zknkCWxv0CtNhWjjnb72HSZdR6WWg%2BsylgLSsAIgQJHlKI5wuDEuvVjNCZA%3D%3D; _clsk=15hm331%7C1709465745293%7C2%7C1%7Cx.clarity.ms%2Fcollect; _ga_12345=GS1.1.1709465737.8.1.1709465754.0.0.0; _ga_88WZ9X400Y=GS1.1.1709465737.8.1.1709465754.43.0.0; _ga_HFH1FZ6EXG=GS1.1.1709465737.8.1.1709465754.43.0.0; __utmz_gtm=utmcsr=google%7Cutmccn=(none)%7Cutmcmd=organic",
    "referer": url,
    "sec-ch-ua": '^\^"Not A(Brand^\^";v=^\^"99^\^", ^\^"Opera^\^";v=^\^"107^\^", ^\^"Chromium^\^";v=^\^"121^\^"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '^\^"Android^\^"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
}

# save the cookies to a file
with open("cookies.json", "w") as file:
    json.dump(cookies, file)

with open("headers.json", "w") as file:
    json.dump(headers, file)

driver.quit()
