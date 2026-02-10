# Topic: Basic Class and Object Creation
# A class is a "blueprint", an object is the "house" built from it.

class MyClass:
    x = 5  # Class attribute

# TRAP: Classes cannot be empty. If you need a placeholder, use 'pass'.
class EmptyClass:
    pass

if __name__ == "__main__":
    # Creating an instance (object)
    p1 = MyClass()
    print(f"Value in p1: {p1.x}")

    # TRAP: Objects are independent. Changing p2 doesn't affect p1.
    p2 = MyClass()
    p2.x = 10
    print(f"p1.x is still {p1.x}, while p2.x is {p2.x}")