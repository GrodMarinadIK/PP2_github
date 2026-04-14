import psycopg2
from connect import get_connection

# 1. Функция поиска (вызывает SELECT из твоей SQL-функции)
def search_contacts(pattern):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        # Вызываем функцию get_contacts_by_pattern
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
        results = cur.fetchall()
        print(f"\nРезультаты поиска для '{pattern}':")
        for row in results:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
        cur.close()
        conn.close()

# 2. Процедура Upsert (вызывает CALL)
def upsert_contact(name, phone):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        print(f"\nКонтакт {name} успешно добавлен/обновлен через процедуру.")
        cur.close()
        conn.close()

# 3. Массовая вставка (принимает списки имен и телефонов)
def bulk_insert(names, phones):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("CALL insert_many_contacts(%s, %s)", (names, phones))
        for notice in conn.notices:
            print(notice) # "Skipping invalid phone: 123"
            
        conn.commit()
        print("\nМассовая вставка завершена.")
        cur.close()
        conn.close()

# 4. Пагинация (LIMIT и OFFSET)
def get_paged_contacts(limit, offset):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        results = cur.fetchall()
        print(f"\nСтраница данных (Limit: {limit}, Offset: {offset}):")
        for row in results:
            print(row)
        cur.close()
        conn.close()

# 5. Удаление через процедуру
def delete_contact(target):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("CALL delete_contact_v2(%s)", (target,))
        conn.commit()
        for notice in conn.notices:
            print(notice) # "Skipping invalid phone: 123"
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Тестируем всё по очереди:
    
    # Поиск
    search_contacts("+") 
    
    # Upsert (создаем нового или меняем Bae)
    upsert_contact("Bae", "+77777777777")
    
    # Пагинация: берем первые 18 записей
    get_paged_contacts(5, 10)
    
    # Массовая вставка (валидация: короткий номер отлетит)
    bulk_insert(["Godjo", "Engin", "Beijin"], ["+71234567890", "123", "+77411459652"]) # "123" не пройдет валидацию
    
    # Удаление
    delete_contact("jfhwihjfhfjwfhwefhwjef")
    # Возвращение
    # upsert_contact("Charles","+7806824280")