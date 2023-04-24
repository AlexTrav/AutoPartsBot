from selenium import webdriver

from bs4 import BeautifulSoup

from db.database import database_instance


urls = {1: "https://www.drom.ru/catalog/bmw/", 2: "https://www.drom.ru/catalog/audi/",
        3: "https://www.drom.ru/catalog/mercedes-benz/", 4: "https://www.drom.ru/catalog/volkswagen/"}


def cars_modifications_main():
    database_instance.connect()

    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    chrome_driver_binary = r"C:\Users\Alex\Desktop\Бизнес\Серёга\Проект\AutoPartsBot\v~0.2\parsing\scripts\chromedriver.exe"

    driver = webdriver.Chrome()

    i = 0

    try:
        driver = webdriver.Chrome(executable_path=chrome_driver_binary,
                                  chrome_options=options)
        car_model_id = 1
        car_submodel_id = 1

        for key in urls:
            driver.get(url=urls[key])

            src = driver.page_source
            soup = BeautifulSoup(src, "lxml")

            cars_models = soup.find_all("a", class_="e64vuai0 css-1i48p5q e104a11t0")

            for car_model in cars_models:

                link = car_model.get("href")
                driver.get(link)

                src = driver.page_source
                soup = BeautifulSoup(src, "lxml")

                cars_submodels = soup.find_all("a", class_="e1ei9t6a1 css-1x6lzas ezhoka60")

                for car_submodel in cars_submodels:

                    sublink = car_submodel.get("href")
                    driver.get(f"{driver.current_url}{sublink}")

                    src = driver.page_source
                    soup = BeautifulSoup(src, "lxml")

                    cars_modifications = soup.find_all("tr", class_="b-table__row b-table_align_top b-table__row_border_bottom b-table__row_padding_size-s")

                    for car_modification in cars_modifications[1:]:
                        ths = car_modification.find_all("th")
                        car_name_configuration = ths[0].getText()
                        database_instance.execute_query(query=f"INSERT INTO cars_modifications(car_submodel_id, name_configuration, name_lc) VALUES ({car_submodel_id}, '{car_name_configuration}', '{car_name_configuration.lower()}')")
                        print(f'id:{i} - car_brand_id:{key} : car_model_id:{car_model_id} : car_submodel_id:{car_submodel_id} : car_name_configuration:{car_name_configuration} - Успешно!')
                        i += 1
                    car_submodel_id += 1
                    driver.back()
                car_model_id += 1

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        database_instance.close()
