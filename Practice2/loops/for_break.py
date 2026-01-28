fruits = ["apple", "banana", "cherry"]

# break (terminate loop) when x is banana
for x in fruits:
    print(x)
    if x == "banana":
        break

# Important: if loop terminated using break, else will be ignored
for x in range(6):
    if x == 3: break
    print(x)
else:
    print("This will NOT be printed")