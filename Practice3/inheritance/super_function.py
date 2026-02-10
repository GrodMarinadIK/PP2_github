# Topic: Using super() to call parent methods
# Requirement: super() usage example

class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

class Student(Person):
    def __init__(self, fname, lname, graduation_year):
        # TRAP: super() refers to the parent class. 
        # It handles the name initialization so we don't repeat code (DRY).
        super().__init__(fname, lname)
        self.graduation_year = graduation_year

    def welcome(self):
        # Accessing parent attributes (firstname) via self
        print(f"Welcome {self.firstname} to the class of {self.graduation_year}")

if __name__ == "__main__":
    s = Student("Alice", "Smith", 2025)
    s.welcome()
    
    
# Key Concept: Using super() to keep parent logic while adding new specific data.