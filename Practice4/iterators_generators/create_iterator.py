class MyNumbers:
    def __init__(self, limit):
        # Store the limit passed during object creation
        self.limit = limit

    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= self.limit: # Use the dynamic limit instead of a hardcoded number
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration

# Using the iterator with a dynamic input
n = int(input("Enter the limit: "))
myclass = MyNumbers(n)
myiter = iter(myclass)

for x in myiter:
    print(x)