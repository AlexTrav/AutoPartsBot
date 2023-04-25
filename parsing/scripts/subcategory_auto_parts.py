from selenium import webdriver

from bs4 import BeautifulSoup

from db.database import database_instance


url = "https://auau.market/section/automobile"


def subcategory_auto_parts_main():
    database_instance.connect()

    options = webdriver.ChromeOptions()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    chrome_driver_binary = r"C:\Users\Alex\Desktop\Бизнес\Серёга\Проект\AutoPartsBot\v~0.2\parsing\scripts\chromedriver.exe"

    driver = webdriver.Chrome()

    try:
        driver = webdriver.Chrome(executable_path=chrome_driver_binary,
                                  chrome_options=options)

        i = 0

        # 1
        driver.get(url=url)

        src = driver.page_source
        soup = BeautifulSoup(src, "lxml")

        subcategory_auto_parts = soup.find_all("ul", class_="more--link")

        for subcategory_auto_part in subcategory_auto_parts:
            lis = subcategory_auto_part.find_all("li")
            for li in lis:
                subcategory_auto_part_name = li.find("a").text
                database_instance.execute_query(query=f"INSERT INTO subcategory_auto_parts(category_id, name, name_lc) VALUES (1, '{subcategory_auto_part_name}', '{subcategory_auto_part_name.lower()}')")
                print(f'id:{i} - category_id:{1} : subcategory_auto_part_name:{subcategory_auto_part_name} - Успешно!')
                i += 1

        # 2
        database_instance.execute_query(query="INSERT INTO subcategory_auto_parts(category_id, name, name_lc) "
                                              "VALUES "
                                              "(2, 'Шины', 'шины'), "
                                              "(2, 'Диски', 'диски')")

        # 3
        database_instance.execute_query(query="INSERT INTO subcategory_auto_parts(category_id, name, name_lc) "
                                              "VALUES "
                                              "(3, 'Масла', 'масла'), "
                                              "(3, 'Смазки', 'смазки'), "
                                              "(3, 'Технические жидкости', 'технические жидкости')")

        # 4
        database_instance.execute_query(query="INSERT INTO subcategory_auto_parts(category_id, name, name_lc) "
                                              "VALUES "
                                              "(4, 'Пленка тонировочная', 'пленка тонировочная'), "
                                              "(4, 'Ведра', 'ведра'), "
                                              "(4, 'Брелоки, чехлы для а/с', 'брелоки, чехлы для а/с'), "
                                              "(4, 'Вентиляторы', 'вентиляторы'), "
                                              "(4, 'Вибро-шумоизоляция', 'вибро-шумоизоляция'), "
                                              "(4, 'Кожгалантерея для документов', 'кожгалантерея для документов'), "
                                              "(4, 'Очки', 'очки'), "
                                              "(4, 'Рамки номерного знака', 'рамки номерного знака'), "
                                              "(4, 'Сувениры', 'сувениры'), "
                                              "(4, 'Сумки', 'сумки'), "
                                              "(4, 'Для интерьера', 'для интерьера'), "
                                              "(4, 'Канистры, воронки', 'канистры, воронки'), "
                                              "(4, 'Щетки, скребки', 'щетки, скребки'), "
                                              "(4, 'Чехлы на сиденья', 'чехлы на сиденья'), "
                                              "(4, 'Коврики', 'коврики')")

        # 5
        database_instance.execute_query(query="INSERT INTO subcategory_auto_parts(category_id, name, name_lc) "
                                              "VALUES "
                                              "(5, 'Акустические провода', 'акустические провода'), "
                                              "(5, 'Сигнализации', 'сигнализации'), "
                                              "(5, 'Трубки для проводки, гофры', 'трубки для проводки, гофры'), "
                                              "(5, 'Батарейки', 'батарейки'), "
                                              "(5, 'Антенны', 'антенны'), "
                                              "(5, 'Вспомогательные системы', 'вспомогательные системы'), "
                                              "(5, 'Алкотестеры', 'алкотестеры'), "
                                              "(5, 'Аудиотехника', 'аудиотехника'), "
                                              "(5, 'Бортовые, маршрутные компьютеры', 'бортовые, маршрутные компьютеры'), "
                                              "(5, 'Парктроники', 'парктроники'), "
                                              "(5, 'Преобразователи напряжения', 'преобразователи напряжения'), "
                                              "(5, 'Радар-детекторы', 'радар-детекторы'), "
                                              "(5, 'Разветвители прикуривателя', 'разветвители прикуривателя'), "
                                              "(5, 'Зажимы крокодил', 'зажимы крокодил'), "
                                              "(5, 'Трубка термоусадочная', 'трубка термоусадочная'), "
                                              "(5, 'Автопылесосы', 'автопылесосы'), "
                                              "(5, 'Кружки-термосы', 'кружки-термосы'), "
                                              "(5, 'Холодильники', 'холодильники'), "
                                              "(5, 'FM-модуляторы, контроллеры', 'fm-модуляторы, контроллеры'), "
                                              "(5, 'Видеорегистраторы', 'видеорегистраторы'), "
                                              "(5, 'Камеры заднего вида', 'камеры заднего вида'), "
                                              "(5, 'Зарядник для телефона', 'зарядник для телефона')")

    except Exception as ex:
        print(f"Исключение: {ex}")

    finally:
        driver.close()
        database_instance.close()
