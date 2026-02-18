# 1. Squares up to N
def square_generator(n):
    for i in range(n + 1):
        yield i ** 2

# 2. Even numbers comma separated
n = int(input("Enter n for evens: "))
evens = (str(i) for i in range(0, n + 1) if i % 2 == 0)
print(", ".join(evens))

# 3. Divisible by 3 and 4
def div_3_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4. Squares from (a) to (b)
def squares_ab(a, b):
    for i in range(a, b + 1):
        yield i ** 2

print("Testing squares from 3 to 6:")
for val in squares_ab(3, 6):
    print(val)

# 5. Countdown from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
