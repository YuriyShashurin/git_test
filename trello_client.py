import sys
import requests

base_url = "https://api.trello.com/1/{}"
auth_params = {
    'key': "178c4d9d396d74865c1d993fa598b865",
    'token': "96996fd5a2988712573982ab3861801cfcb3dc109f1c4810a87184c66c1a9831", }
board_id = "Ihys1GWt"


def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name'])
        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break
    print("Задача " + name + " создана в колонке " + column_name)


def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
        if task_id:
            break

            # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList',
                         data={'value': column['id'], **auth_params})
            break
    print("Задача " + name + " перенесена в колонку " + column_name)

if __name__ == "__main__":
        read()
        create('Добаление новой задачи3', 'Нужно сделать')
        move('Добаление новой задачи3', 'Готово')