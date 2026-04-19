# generate_contacts.py
import random
import csv
import os

current_dir = os.path.dirname(__file__)
path_to_csv = os.path.join(current_dir, "contacts.csv")

names = [
    "Jiwoo", "Bae", "Charles", "Max", "Gabriella", "Nico", "Billy", "Jisu", 
    "Minjeong", "Aeri", "Kyoko", "Izumi", "Umai", "Aya", "Jeongyeon", "Beeji"
]

last_names = [
    "Kim", "Jinsol", "Leclerc", "Verstappen", "Rossi", "Nee", "Herrington", "Choi",
    "Kim", "Uchinaga", "Hori", "Miyamura", "Tanaka", "Saito", "Yoo", "Lee"
]

def generate_fake_csv(filename, count=len(names)):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "last_name", "phone"]) # Headline
        
        for i in range(count):
            name = names[i] if i < len(names) else f"User_{i}"
            last_name = last_names[i] if i < len(last_names) else f"Last_{i}"
            # Generating random part cosisting of 9 digits (like 707 123 45 67)
            random_part = "".join([str(random.randint(0, 9)) for _ in range(9)])
            phone = "+7" + random_part
            writer.writerow([name, last_name, phone])

    print(f"File {filename} for {count} contacts created!")

if __name__ == "__main__":
    generate_fake_csv(path_to_csv)