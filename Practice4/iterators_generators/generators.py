# --- PART 1: Simple Generator ---
def my_generator():
    yield 1
    yield 2
    yield 3

# ❌ INCORRECT WAY: Creating a new generator object in every iteration
print("Incorrect way (always returns 1):")
for _ in range(3):
    # Each call to my_generator() creates a NEW instance starting from the beginning
    print(next(my_generator())) 

print("\n" + "-"*20 + "\n")

# ✅ CORRECT WAY: Create one instance and use it
print("Correct way (returns 1, 2, 3):")
gen_instance = my_generator()
for _ in range(3):
    print(next(gen_instance))

print("\n" + "="*20 + "\n")

# --- PART 2: Fibonacci Generator ---
def fibonacci():
    """
    Infinite sequence generator. 
    Memory efficient because it only stores two variables (a and b).
    """
    a, b = 0, 1
    while True:
        yield a # Pause execution and return current value
        a, b = b, a + b

# Using the singleton instance approach
fib_gen = fibonacci()

print("First 15 Fibonacci numbers:")
for _ in range(15): 
    print(next(fib_gen))