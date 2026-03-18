# read_files.py

def read_line_by_line(filename):
    """Построчное чтение (лучшее для больших файлов)"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                print(line.strip())
    except FileNotFoundError:
        print("Файл не найден.")

def read_methods_demo(filename):
    """Демонстрация других методов чтения"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            # 1. readline() — читает ОДНУ строку
            first_line = f.readline() 
            print(f"Первая строка: {first_line.strip()}")
            
            # 2. readlines() — читает всё оставшееся и делает СПИСОК строк
            remaining_lines = f.readlines()
            print(f"Осталось строк: {len(remaining_lines)}")
    except FileNotFoundError:
        print("Файл не найден.")