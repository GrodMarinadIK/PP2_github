import shutil
import os

def backup_file(source_path, destination_path):
    """Копирует контент + метаданные (copy2)"""
    try:
        shutil.copy2(source_path, destination_path)
        print(f"Бэкап создан: {destination_path}")
    except FileNotFoundError:
        print("Источник не найден.")

def safe_delete_file(filename):
    """Удаление через os.remove с проверкой существования"""
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Файл '{filename}' удален.")
    else:
        print("Удалять нечего, файла нет.")