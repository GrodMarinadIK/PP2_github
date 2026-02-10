# Using lambda with function sorted()

# 1) Sort a list of tuples according to second elements (age)
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
by_age = sorted(students, key=lambda x: x[1])
print(f"Sorted by age: {by_age}")

# 2) Sort a dictionary according to values
prices = {"apple": 50, "orange": 30, "banana": 40}
sorted_prices = sorted(prices.items(), key=lambda item: item[1])
print(f"Sorted prices: {dict(sorted_prices)}")

# 3) Sort according to length, then according to alphabet
words = ["banana", "pie", "apple", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(f"By length: {sorted_words}")

