# Using lambda with function filter()
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Problem: Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Evens: {evens}")  # [2, 4, 6, 8, 10]

# Problem: Keep only words that has length more than 3 symbols
words = ["hi", "python", "ai", "lambda", "code"]
long_words = list(filter(lambda w: len(w) > 3, words))
print(f"Long words: {long_words}")

