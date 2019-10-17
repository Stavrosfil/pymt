from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--no-gpu')
driver = webdriver.Chrome(
    "/usr/lib/chromium-browser/chromedriver", chrome_options=options)

driver.get("http://oasth.gr/#en/stopinfo/screen/13011/")
delay = 10  # seconds
try:
    myElem = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.ID, 'arivals')))
    print("Page is ready!")
except TimeoutException:
    print("Loading took too much time!")

# URL = "http://oasth.gr/#en/stopinfo/screen/13011/"
# driver.get(URL)
# # time.sleep(20)
# # print(driver.page_source)
soup = BeautifulSoup(driver.page_source, 'html5lib')
print(soup.prettify())

print(soup.find_all('ul', attrs={'class': 'arivals'}))
