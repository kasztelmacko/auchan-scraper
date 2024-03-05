from selenium import webdriver
import json
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


# change the user agent not to be detected as a bot
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0")
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

# open the website and wait for cookies to load
driver.get('https://zakupy.auchan.pl/shop/artykuly-spozywcze/mleko-nabial-jaja/maslo-margaryny-tluszcze.c-28821')
time.sleep(3)



# accept cookies popup
action_1 = ActionChains(driver)
element = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
action_1.move_to_element(element).click().perform()
time.sleep(4)

# accept advertisement popup
action_2 = ActionChains(driver)
element = driver.find_element(By.XPATH, "//*[@aria-label='Zamknij okno dialogowe']")
action_2.move_to_element(element).click().perform()

# get cookies when the full website is loaded
start_time = time.time()
while (time.time() - start_time) < 30:
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(3)
cookies = driver.get_cookies()

# save the cookies to a file
with open('cookies.json', 'w') as file:
    json.dump(cookies, file)


driver.quit()

