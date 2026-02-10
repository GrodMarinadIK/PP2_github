# Topic: Multiple inheritance and MRO
# Requirement: Inheriting from more than one class

class Flyer:
    def move(self):
        print("I am flying!")

class Swimmer:
    def move(self):
        print("I am swimming!")

# Inheriting from both
class Duck(Flyer, Swimmer):
    pass

if __name__ == "__main__":
    donald = Duck()
    # TRAP: Which 'move' will it call?
    # Because Flyer is listed first, it calls Flyer.move()
    donald.move() 
    
    # Check the search order:
    print(Duck.mro())
    
    
# Key Concept: A class can inherit from multiple parents.
# TRAP: MRO (Method Resolution Order). 
# If two parents have the same method, Python looks from left to right. (first to last)

