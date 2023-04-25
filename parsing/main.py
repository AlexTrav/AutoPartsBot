# Файл запуска парсинга данных в бд

from scripts import *


def main_parsing():
    cars_brands_main()
    cars_models_main()
    cars_submodels_main()
    cars_modifications_main()

    category_auto_parts_main()
    subcategory_auto_parts_main()
    auto_parts_main()


main_parsing()
