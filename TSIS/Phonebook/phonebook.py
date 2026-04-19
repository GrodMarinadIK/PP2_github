import psycopg2
import csv
import os
import time
from connect import get_connection

# --- ЛОГИКА ИЗ ТВОЕЙ V2 (SQL Функции и Процедуры) ---

def search_contacts(pattern):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            results = cur.fetchall()
            print(f"\nРезультаты поиска для '{pattern}':")
            for row in results:
                # row[0]-id, row[1]-name, row[2]-last_name, row[3]-phone
                print(f"ID: {row[0]} | Name: {row[1]} {row[2]} | Phone: {row[3]}")
            print(f"\nВсего найдено: {len(results)}")
            print("\n" + "="*40)
        conn.close()

def upsert_contact(name, last_name, phone):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("CALL upsert_contact(%s, %s, %s)", (name, last_name, phone))
            conn.commit()
            print(f"\nКонтакт {name} {last_name} успешно добавлен/обновлен.")
        conn.close()

def bulk_insert(names, last_names, phones):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("CALL insert_many_contacts(%s, %s, %s)", (names, last_names, phones))
            for notice in conn.notices:
                print(notice.strip())
            conn.commit()
            print("\nМассовая вставка завершена.")
        conn.close()

def get_paged_contacts(limit, offset):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            results = cur.fetchall()
            print(f"\nСтраница (Limit: {limit}, Offset: {offset}):")
            for row in results:
                print(row)
        conn.close()

def delete_contact_smart():
    target = input("Введите имя или фамилию для удаления: ")
    
    conn = get_connection()
    if not conn: return
    
    with conn.cursor() as cur:
        # 1. Сначала ищем всех, кто подходит под описание
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (target,))
        results = cur.fetchall()
        
        if not results:
            print(f"По запросу '{target}' ничего не найдено.")
            conn.close()
            return

        # 2. Показываем список найденных
        print(f"\nНайдено контактов: {len(results)}")
        for row in results:
            print(f"ID: {row[0]} | {row[1]} {row[2]} | {row[3]}")
        
        # 3. Просим выбрать конкретный ID
        try:
            choice = int(input("\nВведите ID для удаления (или 0 для отмены): "))
            
            if choice == 0:
                print("Удаление отменено.")
                print("\n" + "="*40)
            else:
                # Проверяем, есть ли такой ID в результатах поиска (защита от дурака)
                found_ids = [r[0] for r in results]
                if choice in found_ids:
                    cur.execute("CALL delete_contact_by_id(%s)", (choice,))
                    conn.commit()
                    # Печатаем уведомления из БД (RAISE NOTICE)
                    for notice in conn.notices:
                        print(notice.strip())
                    print("\n" + "="*40)
                else:
                    print("Ошибка: Выбранный ID не входит в список найденных!")
                    print("\n" + "="*40)
                    
        except ValueError:
            print("Ошибка: Нужно ввести число (ID)!")
            print("\n" + "="*40)
    conn.close()

# --- ТЕРМИНАЛЬНЫЙ ИНТЕРФЕЙС ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    print("\n" + "="*40)
    print("      📞 PHONEBOOK TERMINAL SQL")
    print("="*40)
    print(" 1. 📖 Показать контакты (пагинация)")
    print(" 2. 🔍 Поиск по имени/номеру")
    print(" 3. ➕ Добавить или обновить (Upsert)")
    print(" 4. 💣 Удалить контакт (Procedure)")
    print(" 5. 📥 Импорт из CSV")
    print(" 0. 🚪 Выход")
    print("="*40)
    return input("Выбери действие: ")

def run():
    while True:
        choice = main_menu()
        
        if choice == '1':
            try:
                limit = int(input("Сколько записей вывести?: "))
                offset = int(input("Сколько пропустить (offset)?: "))
                get_paged_contacts(limit, offset)
            except ValueError:
                print("Ошибка: вводи числа!")
            input("\nНажми Enter...")

        elif choice == '2':
            pattern = input("Введите паттерн для поиска: ")
            search_contacts(pattern)
            input("\nНажми Enter...")

        elif choice == '3':
            name = input("Имя: ")
            last_name = input("Фамилия: ")
            phone = input("Телефон: ")
            upsert_contact(name, last_name, phone)
            input("\nНажми Enter...")

        elif choice == '4':
            delete_contact_smart()
            input("\nНажми Enter...")

        elif choice == '5':
            csv_name = "TSIS\\Phonebook\\contacts.csv" # Файл лежит в той же папке
            if os.path.exists(csv_name):
                names, last_names, phones = [], [], []
                with open(csv_name, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        names.append(row['name'])
                        last_names.append(row['last_name']) # Добавили чтение фамилии
                        phones.append(row['phone'])
                bulk_insert(names, last_names, phones)
            else:
                print(f"Ошибка: {csv_name} не найден в этой папке!")
            input("\nНажми Enter...")

        elif choice == '0':
            print("Выход... Удачного дня!")
            break
        
        else:
            print("Нет такой команды!")
            time.sleep(1)
        
        clear_screen()

if __name__ == "__main__":
    run()