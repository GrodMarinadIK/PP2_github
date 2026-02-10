# Topic: Method overriding
# Requirement: Show how child classes change parent behavior

class Animal:
    def speak(self):
        print("Animal makes a generic sound")

class Dog(Animal):
    # OVERRIDING: Changing the behavior for Dog
    def speak(self):
        print("Dog barks: Woof!")

class Cat(Animal):
    # OVERRIDING: Changing the behavior for Cat
    def speak(self):
        print("Cat meows: Meow!")

if __name__ == "__main__":
    animals = [Animal(), Dog(), Cat()]
    for animal in animals:
        animal.speak() # Different output for each object!
        
        
# Key Concept: A child class can provide a specific version of a method that is already provided by its parent.