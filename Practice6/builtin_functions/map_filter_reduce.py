# map_filter_reduce.py
from functools import reduce

def process_data():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # 1. Map: возводим в квадрат
    squared = list(map(lambda x: x**2, data)) # [1, 4, 9, ..., 100]

    # 2. Filter: оставляем только те, что больше 50
    big_numbers = list(filter(lambda x: x > 50, squared)) # [64, 81, 100]

    # 3. Reduce: находим их сумму
    total_sum = reduce(lambda x, y: x + y, big_numbers) # 245
    print(f"Изначальная: {data}")
    print(f"Квадраты: {squared}")
    print(f"Только > 50: {big_numbers}")
    print(f"Сумма отобранных: {total_sum}")

if __name__ == "__main__":
    process_data()