# Topic: The __init__() method and 'self'
# 'self' is a reference to the current instance of the class.

class Person:
    # TRAP: __init__ is called AUTOMATICALLY when you create an object.
    # It's a constructor, not a regular method.
    def __init__(self, name, age = 18): # age = 18, means that age has a default value = 18
        self.name = name
        self.age = age

    # TRAP: 'self' MUST be the first argument of any method in a class.
    # You can name it 'abc', but 'self' is the standard (don't be that guy).
    def greet(self):
        print(f"Hello, my name is {self.name}")

if __name__ == "__main__":
    # Standard initialization
    p1 = Person("Marek", 36)
    p1.greet()
    
    # Using default 'age' value from __init__
    p2 = Person("Gabriel")
    print(f"{p2.name} is {p2.age} years old.")