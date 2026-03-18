# write_files.py

def save_data(filename, data):
    """'w' mode: Перезаписывает всё."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"Файл '{filename}' перезаписан.")

def add_data(filename, extra_data):
    """'a' mode: Дописывает в конец."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{extra_data}")
    print(f"Данные добавлены в '{filename}'.")

def create_new_only(filename, data):
    """
    'x' mode: Создает файл ТОЛЬКО если его еще нет.
    Если файл существует — выкинет FileExistsError.
    """
    try:
        with open(filename, "x", encoding="utf-8") as f:
            f.write(data)
        print(f"Файл '{filename}' успешно создан с нуля.")
    except FileExistsError:
        print(f"Ошибка: Файл '{filename}' уже существует! Режим 'x' не дает его затереть.")