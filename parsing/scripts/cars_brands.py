from selenium import webdriver

import requests as rq

# from bs4 import BeautifulSoup

import time

from db.database import database_instance


url = "https://kolesa.kz/zapchasti/prodazha/"


options = webdriver.ChromeOptions()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

chrome_driver_binary = r"C:\Users\Alex\Desktop\Бизнес\Серёга\Проект\AutoPartsBot\v~0.2\parsing\scripts\chromedriver.exe"


driver = webdriver.Chrome(chrome_options=options)
driver.get(chrome_driver_binary)



headers = {


}

try:
    driver.get(url=url)
    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
