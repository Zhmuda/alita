import sqlite3
import re


def get_fio():
    connection = sqlite3.connect('messages.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT fio FROM Users""")
    admins_fio = cursor.fetchall()
    connection.commit()
    connection.close()
    return admins_fio


def get_fio_from_department(department):
    connection = sqlite3.connect('messages.db')
    cursor = connection.cursor()
    cursor.execute("SELECT fio FROM Users WHERE department = ?", (department,))
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def get_id_from_fio(name):
    connection = sqlite3.connect('messages.db')
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM Users WHERE fio = ?", (name,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result


def get_users():
    connection = sqlite3.connect('messages.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Users""")
    users = cursor.fetchall()
    connection.commit()
    connection.close()
    return users


def get_id():
    connection = sqlite3.connect('messages.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT id FROM Users""")
    ids = cursor.fetchall()
    connection.commit()
    connection.close()
    return ids


def get_user_id():
    connection = sqlite3.connect('messages.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT from_who_id FROM Messages""")
    ids = cursor.fetchall()
    connection.commit()
    connection.close()
    return ids


def get_rows_by_value(id_to_check, value_to_check):
    # Установить соединение с базой данных
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    # Выполнить SQL-запрос с условием WHERE для получения строк
    cursor.execute("SELECT * FROM messages WHERE to_who_id = ? AND approved = ?", (id_to_check, value_to_check))
    rows = cursor.fetchall()
    conn.close()
    # Вывести строки, удовлетворяющие условию
    return rows

    # Закрыть соединение с базой данных


def get_notifications(id):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    # Выполнить SQL-запрос
    id_to_check = id
    cursor.execute(f"SELECT * FROM Messages WHERE to_who_id = {id_to_check}")
    result = cursor.fetchall()
    # Закрыть соединение с базой данных
    conn.close()
    return result


def delete_notifications(user_id):
    # Подключаемся к базе данных
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    # Удаляем записи, где значение столбца 'status' равно 1, 2 или 4
    cursor.execute("DELETE FROM Messages WHERE approved IN (1, 2, 4) AND to_who_id = ?", (user_id,))

    # Сохраняем изменения и закрываем соединение с базой данных
    conn.commit()
    print("Переменные Python успешно удалены из таблицы messages")
    conn.close()


def insert_messages(to_who_id, from_who_id, from_who_username, message_text, date, approved):
    try:
        connection = sqlite3.connect('messages.db')
        cursor = connection.cursor()
        print("Подключен к SQLite")
        sqlite_insert_with_param = """
                            INSERT INTO messages
                            (to_who_id, from_who_id, from_who_username, message_text, date, approved)
                            VALUES
                            (?, ?, ?, ?, ?, ?);"""
        data_tuple = (to_who_id, from_who_id, from_who_username, message_text, date, approved)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        connection.commit()
        print("Переменные Python успешно вставлены в таблицу messages")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def insert_new_admin(id, username, fio, department):
    try:
        connection = sqlite3.connect('messages.db')
        cursor = connection.cursor()
        print("Подключен к SQLite")
        sqlite_insert_with_param = """
                            INSERT INTO Users
                            (id, username, fio, department)
                            VALUES
                            (?, ?, ?, ?);"""
        data_tuple = (id, username, fio, department)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        connection.commit()
        cursor.close()
        return "Админ успешно добавлен"
    except sqlite3.Error as error:
        return f'произошла ошибка: {error}'


def get_rows_by_id_and_status(user_id, statuses):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    # Выполнение SQL-запроса с параметрами
    cursor.execute(
        "SELECT * FROM messages WHERE to_who_id=? AND approved IN ({})".format(','.join('?' for _ in statuses)),
        [user_id] + statuses)

    # Получение результатов запроса
    rows = cursor.fetchall()

    # Закрытие соединения с базой данных
    conn.close()

    return rows


def update_value_in_database(id_to_update, new_value):
    try:
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE messages SET approved = ? WHERE id = ?", (new_value, id_to_update))
        conn.commit()
        conn.close()
        print("Значение столбца успешно обновлено!")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def parse_and_insert_numbers(conn):
    cursor = conn.cursor()

    # Получение данных из таблицы messages
    select_messages_query = 'SELECT id, to_who_id, message_text FROM messages'
    cursor.execute(select_messages_query)
    messages = cursor.fetchall()

    # Регулярное выражение для поиска чисел в тексте сообщения
    number_pattern = re.compile(r'\b\d{3,}\b|\b\d+-\d+-\d+-\d+/\d+\b')

    # Парсинг и вставка данных в новую таблицу
    for message_id, to_who_id, message_text in messages:
        numbers = [match.group() for match in number_pattern.finditer(message_text)]
        for number in numbers:
            # print(message_text)
            # Проверка существует ли уже такой message_id в таблице message_numbers
            check_query = 'SELECT EXISTS(SELECT 1 FROM message_numbers WHERE message_id = ?)'
            cursor.execute(check_query, (message_id,))
            exists = cursor.fetchone()[0]

            # Вставка новой записи, если такого message_id нет
            if not exists:
                # print(1)
                insert_query = 'INSERT INTO message_numbers (message_id, messages_number, to_who_id) VALUES (?, ?, ?)'
                cursor.execute(insert_query, (message_id, number, to_who_id))

    # Сохранение изменений
    conn.commit()


def delete_all_from_table():
    # подключение к базе данных
    conn = sqlite3.connect('messages.db')

    # создание объекта курсора
    cursor = conn.cursor()

    # выполнение SQL-запроса для удаления всех данных из таблицы
    cursor.execute(f'DELETE FROM message_numbers')

    # сохранение изменений в базе данных
    conn.commit()

    # закрытие соединения с базой данных
    conn.close()


def does_message_exist(conn, to_who_id, message_text):
    cursor = conn.cursor()

    # Регулярное выражение для поиска чисел в тексте сообщения
    number_pattern = re.compile(r'\b\d{3,}\b|\b\d+-\d+-\d+-\d+/\d+\b')
    numbers = set(match.group() for match in number_pattern.finditer(message_text))

    if not numbers:
        # Если чисел в сообщении нет, то возвращаем False
        return False

    print(numbers)

    # Поиск сообщений для данного получателя с такими же числами
    select_query = '''
        SELECT COUNT(*) FROM messages
        WHERE to_who_id = ? AND id IN (
            SELECT message_id FROM message_numbers
            WHERE messages_number IN ({})
            GROUP BY message_id
            HAVING COUNT(DISTINCT messages_number) = {}
        )
    '''.format(', '.join('?' * len(numbers)), len(numbers))

    cursor.execute(select_query, (to_who_id,) + tuple(numbers))
    count = cursor.fetchone()[0]
    print(count)
    return count > 0


def get_outdated(id):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("SELECT from_who_id, message_text FROM messages WHERE to_who_id=? AND approved IN (0, 5)", (id,))
    values = cursor.fetchall()
    conn.close()
    return values


def delete_outdated(id):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE to_who_id=? AND approved IN (0, 5)", (id,))
    conn.commit()
    conn.close()