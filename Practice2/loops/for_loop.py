# loop through list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# loop through string (strings are iterable)
for letter in "banana":
    print(letter)

# function range():
# range(6) -> from 0 to 5
# range(2, 6) -> from 2 to 5
# range(2, 30, 3) -> from 2 to 30 with step 3
for x in range(2, 30, 3):
    print(x)

# Else in loop for (execute when loop end)
for x in range(6):
    print(x)
else:
    print("Finally finished!")

# (Nested Loops)
adj = ["red", "big", "tasty"]
for x in adj:
    for y in fruits:
        print(x, y) # Every combination

# Заглушка pass
for x in [0, 1, 2]:
    pass # for avoiding errors for empty loop