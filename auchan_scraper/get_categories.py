import json
import logging
import re
import time
from typing import Dict, List, Optional, Tuple

from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("get_categories_debug.log"), logging.StreamHandler()],
)


def get_url_segments(url: str) -> str:
    pattern = r"(\/shop\/[^.]+)\.c\-\d+"
    match = re.search(pattern, url)
    if match:
        return f"{match.group(1)}/"
    return None


def initialize_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
    )
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver


def accept_popups(
    driver: webdriver.Chrome, url: Optional[str] = None
) -> webdriver.Chrome:
    if url:
        driver.get(url)
    xpath_selectors = [
        "//*[@id='onetrust-accept-btn-handler']",
        "//*[@aria-label='Zamknij okno dialogowe']",
        "//*[@id='accept-recommended-btn-handler']",
    ]

    for xpath_selector in xpath_selectors:
        elements = driver.find_elements(By.XPATH, xpath_selector)
        if not elements:
            logging.warning(f"Popup {xpath_selector} not present")
            continue
        try:
            logging.info(f"Clicking on popup {xpath_selector}")
            wait = WebDriverWait(driver, timeout=10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_selector)))
            element.click()
        except (
            NoSuchElementException,
            TimeoutException,
            ElementClickInterceptedException,
        ) as e:
            print(xpath_selector, e)
            logging.error(f"Popup {xpath_selector} not found: {e}")

    return driver


def elements_have_text(driver: webdriver.Chrome, selector: str):
    # we need to scroll to make text visible
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.05)
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
    return all(element.text.strip() != "" for element in elements)


def get_categories(
    url: str, limit: Optional[int] = None
) -> Tuple[List[Dict], List[Dict]]:
    driver = initialize_driver()

    driver = accept_popups(driver, url=url)

    logging.info(f"Visiting {url}")

    cat_selector = f'a[href*="{get_url_segments(url)}"]'
    wait = WebDriverWait(driver, timeout=10)
    wait.until(lambda driver: elements_have_text(driver, cat_selector))

    categories = driver.find_elements(By.CSS_SELECTOR, cat_selector)

    if not limit:
        limit = len(categories)

    categories = [
        category for cat_num, category in enumerate(categories) if cat_num < limit
    ]

    categories = [
        {
            "category": category.text,
            "url": category.get_attribute("href"),
            "subcategories": [],
        }
        for category in categories
    ]

    logging.info(str(categories))

    for category in categories:
        logging.info(f"Visiting {category['url']}")
        driver.get(category["url"])
        subcat_selector = f'a[href*="{get_url_segments(category["url"])}"]'

        wait = WebDriverWait(driver, timeout=10)
        wait.until(lambda driver: elements_have_text(driver, subcat_selector))

        subcategories = driver.find_elements(By.CSS_SELECTOR, subcat_selector)

        category["subcategories"] = [
            {"category": subcategory.text, "url": subcategory.get_attribute("href")}
            for subcategory in subcategories
        ]

    cookies = driver.get_cookies()

    driver.quit()
    return categories, cookies


if __name__ == "__main__":
    # sample urls
    # https://zakupy.auchan.pl/shop/artykuly-spozywcze.c-11908
    # https://zakupy.auchan.pl/shop/artykuly-spozywcze/pieczywo-i-wyroby-cukiernicze.c-13702
    # https://zakupy.auchan.pl/shop/artykuly-spozywcze/pieczywo-i-wyroby-cukiernicze/chleb.c-13705
    url = "https://zakupy.auchan.pl/shop/artykuly-spozywcze.c-11908"

    categories, cookies = get_categories(url)
    with open("categories.json", "w") as categories_file:
        json.dump(categories, categories_file)

    with open("cookies.json", "w") as cookies_file:
        json.dump(cookies, cookies_file)
