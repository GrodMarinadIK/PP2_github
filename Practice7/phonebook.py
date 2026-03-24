# phonebook.py

import psycopg2
import csv
import os
from connect import get_connection

# --- CREATE ---
def create_table():
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL UNIQUE
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

# --- INSERT (CSV) ---
def import_from_csv(file_path):
    conn = get_connection()
    if not conn: return
    cur = conn.cursor()
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
                        (row['name'], row['phone']))
    conn.commit()
    cur.close()
    conn.close()

# --- INSERT (Console) ---
def add_manual():
    name = input("Имя: "); phone = input("Телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close(); conn.close()

# --- UPDATE ---
def update_contact(name, new_phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    conn.commit()
    cur.close(); conn.close()

# --- QUERY (Search) ---
def search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE name LIKE %s OR phone LIKE %s", 
                (f'%{pattern}%', f'{pattern}%'))
    for row in cur.fetchall():
        print(row)
    cur.close(); conn.close()

# --- DELETE ---
def delete_contact(target):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name = %s OR phone = %s", (target, target))
    conn.commit()
    cur.close(); conn.close()

if __name__ == "__main__":
    create_table()
    # It's the place for checking any function
    print("База готова к работе!")
    current_dir = os.path.dirname(__file__)
    path_to_csv = os.path.join(current_dir, "contacts.csv")
    import_from_csv(path_to_csv)