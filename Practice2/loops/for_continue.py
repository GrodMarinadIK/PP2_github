fruits = ["apple", "banana", "cherry"]

# Skip banana, other values printed
for x in fruits:
    if x == "banana":
        continue
    print(x)