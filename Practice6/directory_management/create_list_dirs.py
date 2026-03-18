import os
from pathlib import Path

def create_and_manage():
    # 1. os.getcwd() и os.chdir() — Навигация
    start_dir = os.getcwd()
    print(f"Старт в: {start_dir}")

    # 2. os.mkdir() vs os.makedirs() — Создание
    # mkdir создаст одну папку, makedirs — всё дерево
    path_tree = "data/logs/2026"
    os.makedirs(path_tree, exist_ok=True) 
    
    os.chdir("data") # Прыгаем внутрь
    print(f"Сейчас я в: {os.getcwd()}")

    # 3. os.listdir() — Листинг
    items = os.listdir(".") # Список файлов в текущей папке
    print(f"Содержимое 'data': {items}")

    # 4. pathlib — современный подход
    p = Path("logs/2026")
    print(f"Родитель через pathlib: {p.parent}")

    # Возвращаемся на базу
    os.chdir(start_dir)

def cleanup_basics(folder):
    # 5. os.rmdir() — Удаление (только если папка пустая!)
    if os.path.exists(folder):
        try:
            os.rmdir(folder)
            print(f"Пустая папка {folder} удалена.")
        except OSError:
            print(f"Не удалось удалить {folder}: папка не пуста.")

if __name__ == "__main__":
    create_and_manage()