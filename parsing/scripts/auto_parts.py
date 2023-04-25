from selenium import webdriver

from bs4 import BeautifulSoup

from db.database import database_instance

urls = ["https://auau.market/section/automobile",
        ['https://almaty.kolesa-darom.ru/catalog/avto/shiny/', 'https://almaty.kolesa-darom.ru/catalog/avto/diski/'],
        "https://topdetal.ru/catalog/masla_smazki_i_tekh_zhidkosti/", "https://topdetal.ru/catalog/aksessuary/",
        "https://topdetal.ru/catalog/avtoelektronika/"]


def auto_parts_main():
    database_instance.connect()

    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    chrome_driver_binary = r"C:\Users\Alex\Desktop\Бизнес\Серёга\Проект\AutoPartsBot\v~0.2\parsing\scripts\chromedriver.exe"

    driver = webdriver.Chrome(executable_path=chrome_driver_binary,
                              chrome_options=options)
    try:

        i = 1

    # 1
        driver.get(url=urls[0])
        subcategory_id = 39

        src = driver.page_source
        soup = BeautifulSoup(src, "lxml")

        subcategory_auto_parts = soup.find_all("ul", class_="more--link")

        for subcategory_auto_part in subcategory_auto_parts[2:]:
            lis = subcategory_auto_part.find_all("li")
            for li in lis[12:]:
                sublink = li.find("a").get("href")
                driver.get(url=f"https://auau.market{sublink}")

                src = driver.page_source
                soup = BeautifulSoup(src, "lxml")

                auto_parts = soup.find_all("a", class_="product-preview")

                for auto_part in auto_parts:

                    sublink2 = auto_part.get("href")
                    driver.get(url=f"https://auau.market{sublink2}")

                    src = driver.page_source
                    soup = BeautifulSoup(src, "lxml")

                    if soup.find("div", class_="product-card__title cmt-1 order-lg-1 cmb-lg-4 cmt-lg-0"):
                        name = soup.find("div", class_="product-card__title cmt-1 order-lg-1 cmb-lg-4 cmt-lg-0").text.replace("'", '').replace('"', '')
                    else:
                        name = ''

                    description = ''
                    if soup.find("div", class_="desc"):
                        if soup.find("div", class_="desc").find("div", class_="row").find("div", class_="col-sm-12 col-md-12"):
                            ps = soup.find("div", class_="desc").find("div", class_="row").find("div", class_="col-sm-12 col-md-12").find_all("p")
                            for p in ps:
                                description += p.text.replace("'", '').replace('"', '')
                        elif soup.find("div", class_="desc").find("div", class_="row").find("div", class_="col-sm-12 col-md-6"):
                            ps = soup.find("div", class_="desc").find("div", class_="row").find("div", class_="col-sm-12 col-md-6").find_all("p")
                            for p in ps:
                                description += p.text

                    if soup.find("img", class_="product-preview__img"):
                        photo = soup.find("img", class_="product-preview__img").get("src")
                    else:
                        photo = ''
                    if soup.find("div", class_="price"):
                        price = soup.find("div", class_="price").text[:-1].replace('\n', '').replace(' ', '').strip()
                    else:
                        price = ''
                    if soup.find("div", class_="spec__description"):
                        article = soup.find("div", class_="spec__description").text
                    else:
                        article = ''
                    if name and price:
                        database_instance.execute_query(query=f"INSERT INTO auto_parts(subcategory_id, name, article, description, price, photo, count, name_lc) VALUES ({subcategory_id}, '{name}', '{article}', '{description}', {int(price)}, '{photo}', 10, '{name.lower()}')")
                        print(f'id:{i} - category_id:{1} : subcategory_id:{subcategory_id} : name:{name}, description:{description}, photo:{photo}, price:{price} - Успешно!')
                        i += 1
                subcategory_id += 1

    # 2
        subcategory_id = 41
        driver.get(url=urls[1][1])

        src = driver.page_source
        soup = BeautifulSoup(src, "lxml")

        datas = soup.find_all("a", class_="product-card-properties__main")

        for data in datas[2:]:
            sublink = data.get("href")
            driver.get(url=f"https://almaty.kolesa-darom.ru{sublink}")

            src = driver.page_source
            soup = BeautifulSoup(src, "lxml")

            name = soup.find("h1", class_="product-information__title").text.replace("\n", "").replace("\t", "").strip()
            brand = soup.find("span", class_="dots-leaders-item__right").text.replace("\n", "").replace("\t", "").strip()
            description = ""
            if soup.find("div", class_="content-2-cols__item"):
                if soup.find("div", class_="content-2-cols__item").find("p"):
                    description = soup.find("div", class_="content-2-cols__item").find("p").text.replace("\n", "").replace("\t", "").strip()
            price = soup.find("span", class_="product-price-summ").text.replace('\n', '').replace(' ', '').replace('\xa0', '').strip()
            photo = soup.find("img", class_="default-size-image").get("src")
            database_instance.execute_query(query=f"INSERT INTO auto_parts(subcategory_id, name, brand, description, price, photo, count, name_lc) VALUES ({subcategory_id}, '{name[:100]}', '{brand[:100]}', '{description}', {int(price)}, '{photo}', 10, '{name[:100].lower()}')")
            print(f'id:{i} - category_id:{2} : subcategory_id:{subcategory_id} : name:{name} : brand:{brand} : description:{description}, photo:{photo}, price:{price} - Успешно!')
            i += 1

    # 3
            subcategory_id = 42
            driver.get(url=urls[2])

            src = driver.page_source
            soup = BeautifulSoup(src, "lxml")

            datas = soup.find_all("span", class_="bx_catalog_text_title")
            for data1 in datas:
                sublink = data1.find("a").get("href")
                driver.get(f"https://topdetal.ru/{sublink}")

                src = driver.page_source
                soup = BeautifulSoup(src, "lxml")

                datas2 = soup.find_all("div", class_="bx_catalog_item_title")

                for data2 in datas2:
                    sublink2 = data2.find("a").get("href")
                    driver.get(f"https://topdetal.ru/{sublink2}")

                    src = driver.page_source
                    soup = BeautifulSoup(src, "lxml")

                    name = soup.find("h1").find("span").text
                    if soup.find("u", class_="get-brand-link"):
                        brand = soup.find("u", class_="get-brand-link").text
                    elif soup.find("li", class_="prop_BREND"):
                        brand = soup.find("li", class_="prop_BREND").find("b").text
                    else:
                        brand = ""
                    if soup.find("div", class_="bx_tab_item active").find("div"):
                        description = soup.find("div", class_="bx_tab_item active").find("div").text.replace("\n", "").replace(
                            "\t", "").strip()
                    else:
                        description = ""
                    price = soup.find_all("div", class_="item_current_price")[1].text
                    photo = "https://topdetal.ru" + soup.find("span", class_="bx_bigimages_aligner").find("img").get("src")

                    database_instance.execute_query(
                        query=f"INSERT INTO auto_parts(subcategory_id, name, brand, description, price, photo, count, name_lc) VALUES ({subcategory_id}, '{name[:100]}', '{brand[:100]}', '{description}', {int(price)}, '{photo}', 10, '{name[:100].lower()}')")
                    print(
                        f'id:{i} - category_id:{3} : subcategory_id:{subcategory_id} : name:{name} : brand:{brand} : description:{description}, photo:{photo}, price:{price} - Успешно!')
                    i += 1
                subcategory_id += 1

    # 4
        subcategory_id = 45
        driver.get(url=urls[3])

        src = driver.page_source
        soup = BeautifulSoup(src, "lxml")

        datas = soup.find_all("span", class_="bx_catalog_text_title")
        for data in datas:
            sublink = data.find("a").get("href")
            driver.get(f"https://topdetal.ru/{sublink}")

            src = driver.page_source
            soup = BeautifulSoup(src, "lxml")

            datas2 = soup.find_all("div", class_="bx_catalog_item_title")

            for data2 in datas2:
                sublink2 = data2.find("a").get("href")
                driver.get(f"https://topdetal.ru/{sublink2}")

                src = driver.page_source
                soup = BeautifulSoup(src, "lxml")

                name = soup.find("h1").find("span").text
                if soup.find("u", class_="get-brand-link"):
                    brand = soup.find("u", class_="get-brand-link").text
                elif soup.find("li", class_="prop_BREND"):
                    brand = soup.find("li", class_="prop_BREND").find("b").text
                else:
                    brand = ""
                if soup.find("div", class_="bx_tab_item active").find("div"):
                    description = soup.find("div", class_="bx_tab_item active").find("div").text.replace("\n", "").replace(
                        "\t", "").strip()
                else:
                    description = ""
                price = soup.find_all("div", class_="item_current_price")[1].text.replace(" ", "")
                photo = "https://topdetal.ru" + soup.find("span", class_="bx_bigimages_aligner").find("img").get("src")

                database_instance.execute_query(query=f"INSERT INTO auto_parts(subcategory_id, name, brand, description, price, photo, count, name_lc) VALUES ({subcategory_id}, '{name[:100]}', '{brand[:100]}', '{description}', {int(price)}, '{photo}', 10, '{name[:100].lower()}')")
                print(f'id:{i} - category_id:{3} : subcategory_id:{subcategory_id} : name:{name} : brand:{brand} : description:{description}, photo:{photo}, price:{int(price)} - Успешно!')
                i += 1
            subcategory_id += 1

    # 5
        subcategory_id = 60
        driver.get(url=urls[4])

        src = driver.page_source
        soup = BeautifulSoup(src, "lxml")

        datas = soup.find_all("span", class_="bx_catalog_text_title")
        for data in datas:
            sublink = data.find("a").get("href")
            driver.get(f"https://topdetal.ru/{sublink}")

            src = driver.page_source
            soup = BeautifulSoup(src, "lxml")

            datas2 = soup.find_all("div", class_="bx_catalog_item_title")

            for data2 in datas2:
                sublink2 = data2.find("a").get("href")
                driver.get(f"https://topdetal.ru/{sublink2}")

                src = driver.page_source
                soup = BeautifulSoup(src, "lxml")

                name = soup.find("h1").find("span").text
                if soup.find("u", class_="get-brand-link"):
                    brand = soup.find("u", class_="get-brand-link").text
                elif soup.find("li", class_="prop_BREND"):
                    brand = soup.find("li", class_="prop_BREND").find("b").text
                else:
                    brand = ""
                if soup.find("div", class_="bx_tab_item active").find("div"):
                    description = soup.find("div", class_="bx_tab_item active").find("div").text.replace("\n", "").replace(
                        "\t", "").strip()
                else:
                    description = ""
                price = soup.find_all("div", class_="item_current_price")[1].text.replace(" ", "")
                photo = "https://topdetal.ru" + soup.find("span", class_="bx_bigimages_aligner").find("img").get("src")

                database_instance.execute_query(query=f"INSERT INTO auto_parts(subcategory_id, name, brand, description, price, photo, count, name_lc) VALUES ({subcategory_id}, '{name[:100]}', '{brand[:100]}', '{description}', {int(price)}, '{photo}', 10, '{name[:100].lower()}')")
                print(f'id:{i} - category_id:{5} : subcategory_id:{subcategory_id} : name:{name} : brand:{brand} : description:{description}, photo:{photo}, price:{int(price)} - Успешно!')
                i += 1
            subcategory_id += 1

    except Exception as ex:
        print(f"Исключение: {ex}")

    finally:
        driver.close()
        database_instance.close()
