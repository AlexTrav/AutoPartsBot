from selenium import webdriver

from bs4 import BeautifulSoup

from db.database import database_instance

urls = {1: "https://www.drom.ru/catalog/bmw/", 2: "https://www.drom.ru/catalog/audi/",
        3: "https://www.drom.ru/catalog/mercedes-benz/", 4: "https://www.drom.ru/catalog/volkswagen/"}


def cars_models_main():
    database_instance.connect()

    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    chrome_driver_binary = r"C:\Users\Alex\Desktop\Бизнес\Серёга\Проект\AutoPartsBot\v~0.2\parsing\scripts\chromedriver.exe"

    driver = webdriver.Chrome()

    try:
        driver = webdriver.Chrome(executable_path=chrome_driver_binary,
                                  chrome_options=options)

        i = 0

        for key in urls:
            driver.get(url=urls[key])

            src = driver.page_source
            soup = BeautifulSoup(src, "lxml")

            cars_models = soup.find_all("a", class_="e64vuai0 css-1i48p5q e104a11t0")

            for car_model in cars_models:
                car_model_name = car_model.text
                database_instance.execute_query(query=f"INSERT INTO cars_models(car_brand_id, name, name_lc) VALUES ({key}, '{car_model_name}', '{car_model_name.lower()}')")
                print(f'{i} - {key} : {car_model_name} - Успешно!')
                i += 1

    except Exception as ex:
        print(f"Исключение: {ex}")

    finally:
        driver.close()
        database_instance.close()
