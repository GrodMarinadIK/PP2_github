# This file acts as a module library
def greeting(name):
    print("Hello, " + name)

person1 = {
    "first_name": "Khidir",
    "last_name" : "Karawida",
    "age": 36,
    "country": "Norway"
}

# This part only runs if you execute THIS file directly
if __name__ == "__main__":
    print("--- Module executed directly ---")
    greeting(person1["first_name"])
