from db.database import database_instance


def category_auto_parts_main():
    try:
        database_instance.connect()
        database_instance.execute_query(query="INSERT INTO category_auto_parts(name, name_lc) "
                                              "VALUES "
                                              "('Автозапчасти', 'автозапчасти'), "
                                              "('Шины и Диски', 'шины и диски'), "
                                              "('Масла, смазки и тех. жидкости', 'масла, смазки и тех. жидкости'), "
                                              "('Аксессуары', 'аксессуары'), "
                                              "('Автоэлектроника', 'автоэлектроника')")

    except Exception as ex:
        print(f"Исключение: {ex}")

    finally:
        database_instance.close()

