# Файл служащий для реализации возвращения из формы в форму

# Кнопка назад

# Список последних состояний
STATES_LIST = []


# Добавить состояние
def add_state(state):
    STATES_LIST.append(state)


# Удалить состояние
def delete_state():
    STATES_LIST.pop(-1)


# Удалить все состояния
def delete_all_states():
    if not STATES_LIST:
        STATES_LIST.clear()
