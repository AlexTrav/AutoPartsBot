from selenium import webdriver

from bs4 import BeautifulSoup

from db.database import database_instance


urls = {1: "https://www.drom.ru/catalog/bmw/", 2: "https://www.drom.ru/catalog/audi/",
        3: "https://www.drom.ru/catalog/mercedes-benz/", 4: "https://www.drom.ru/catalog/volkswagen/"}


def cars_submodels_main():
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

                cars_submodels = soup.find_all("span", class_="css-1089mxj e1ei9t6a2")

                for car_submodel in cars_submodels:
                    car_submodel_name = car_submodel.text
                    car_submodel_name = car_submodel_name.replace("\r", "")
                    car_submodel_name = car_submodel_name.replace("\n", " ")
                    database_instance.execute_query(query=f"INSERT INTO cars_submodels(car_model_id, name, name_lc) VALUES ({car_model_id}, '{car_submodel_name}', '{car_submodel_name.lower()}')")
                    print(f'id:{i} - car_brand_id:{key} : car_model_id:{car_model_id} : {car_submodel_name} - Успешно!')
                    i += 1

                car_model_id += 1

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        database_instance.close()
