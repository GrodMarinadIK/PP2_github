# Using lambda with function map()
numbers = [1, 2, 3, 4, 5]

# Problem: to raise every number to 2nd power
squared = list(map(lambda x: x**2, numbers))
print(f"Squares: {squared}")  # [1, 4, 9, 16, 25]

# Problem: transform a list of names to a list of greetings
names = ["Alice", "Bob", "Charlie"]
greetings = list(map(lambda name: f"Hello, {name}!", names))
print(greetings)

