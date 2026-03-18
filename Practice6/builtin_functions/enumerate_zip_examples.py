# enumerate_zip_examples.py

def show_zip_and_enumerate():
    names = ["GrodMarinad2k", "Dizzy", "Lion"]
    cities = ["Almaty", "Moscow", "Innopolis"]
    scores = [100, 85, 90]

    print("--- Использование zip ---")
    # Склеиваем три списка в один поток кортежей
    combined = zip(names, cities, scores)
    for name, city, score in combined:
        print(f"Юзер {name} живет в {city} и набрал {score} баллов.")

    print("\n--- Использование enumerate ---")
    # Даем каждому юзеру порядковый номер (ранг)
    for index, name in enumerate(names, start=1):
        print(f"Место №{index}: {name}")

    print("\n--- Комбо: enumerate + zip ---")
    # Идеально для формирования таблиц
    for i, (name, city) in enumerate(zip(names, cities), 1):
        print(f"{i}. {name} (Локация: {city})")

if __name__ == "__main__":
    show_zip_and_enumerate()