# Topic: Basic Inheritance
# Requirement: Parent and child class relationships

class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(f"Full Name: {self.firstname} {self.lastname}")

# Student inherits everything from Person 
class Student(Person):
    # TRAP: If no __init__ is defined, it uses the Parent's __init__
    pass

if __name__ == "__main__":
    x = Student("Mike", "Olsen")
    x.printname()
    

# Key Concept: Inheritance represents an "Is-A" relationship (A Student is a Person).