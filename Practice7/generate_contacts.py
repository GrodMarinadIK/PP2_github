import random
import csv
import os

current_dir = os.path.dirname(__file__)
path_to_csv = os.path.join(current_dir, "contacts.csv")

names = [
    "Jiwoo", "Bae", "Charles", "Max", "Gabriella", "Nico", "Billy", 
    "Jisu", "Minjeong", "Aeri", "Kyoko", "Izumi", "Umai", "Aya", "Jeongyeon"
]

def generate_fake_csv(filename, count=15):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "phone"]) # Заголовок
        
        for i in range(count):
            name = names[i] if i < len(names) else f"User_{i}"
            # Генерируем рандомную часть из 9 цифр (типа 707 123 45 67)
            random_part = "".join([str(random.randint(0, 9)) for _ in range(9)])
            phone = "+7" + random_part
            writer.writerow([name, phone])
            
    print(f"Файл {filename} на {count} контактов готов!")

if __name__ == "__main__":
    generate_fake_csv(path_to_csv)