# Topic: Object Methods and String Representation

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # TRAP: Without __str__, print(obj) returns <__main__.Person object at 0x...>
    # This method defines what the user sees when printing the object.
    def __str__(self):
        return f"Person: {self.name}, Age: {self.age}"

    def update_age(self, new_age):
        self.age = new_age

if __name__ == "__main__":
    p1 = Person("Scattman", 25)
    print(p1)  # Triggering __str__

    # TRAP: You can delete object properties or even the object itself using 'del'
    del p1.age
    # print(p1.age) # This would raise an AttributeError now!