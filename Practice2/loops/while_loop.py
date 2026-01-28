# There are 2 loops in Python: while and for

# While is for cases when you want loop to stop after some condition, 
# or you do not know what is size of iterable item 

k = 1

while k < 5:
    print(f"k now is = {k}")
    k = k + 1
print()

# you could write inside while loop code that belongs to loop-block:
i = 1
while i < 5:
    print(f"i now is = {i}")
    print(f"2 to the power of {i} is: {2**i}")
    i = i + 1
else:
    print()
    print("i is no longer less than 5")