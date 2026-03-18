import os
import shutil

def handle_files(source, target_dir):
    # 1. Подготовка места 
    os.makedirs(target_dir, exist_ok=True)
    
    # Конструируем путь
    destination = os.path.join(target_dir, os.path.basename(source))

    # 2. shutil.move() — Перемещение или переименование
    if os.path.exists(source):
        shutil.move(source, destination)
        print(f"Файл улетел в: {destination}")
    else:
        print("Источник не найден!")

def heavy_cleanup(folder):
    # 3. shutil.rmtree() — Рекурсивное удаление
    # В отличие от os.rmdir, этот снесет папку, даже если в ней миллион файлов
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"Папка {folder} и всё её содержимое стерты в порошок.")

if __name__ == "__main__":
    # Пример: перемещаем какой-нибудь лог в архив
    # handle_files("test.txt", "archive")
    # heavy_cleanup("data")
    pass