import sqlite3
import re


def change_id():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    # Задаем значения для замены
    old_value = 'goldanna'
    new_value = 'goldanna0'

    # Обновляем значение в столбце для всех строк в таблице
    cursor.execute("UPDATE Users SET username = ? WHERE username = ?", (new_value, old_value))

    # Сохраняем изменения в базе данных и закрываем соединение
    conn.commit()
    conn.close()


change_id()