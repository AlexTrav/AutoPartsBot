from db.database import database_instance


def cars_brands_main():
    try:
        database_instance.connect()
        database_instance.execute_query(query="INSERT INTO cars_brands(name, name_lc) "
                                              "VALUES "
                                              "('BMW', 'bmw'), "
                                              "('AUDI', 'audi'), "
                                              "('MERCEDES', 'mercedes'), "
                                              "('VOLKSWAGEN', 'volkswagen')")

    except Exception as ex:
        print(f"Исключение: {ex}")

    finally:
        database_instance.close()

