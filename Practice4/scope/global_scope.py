# Global variable
x = 300

def myfunc():
    # We can read global x without any special keywords
    print(f"Reading global x: {x}")

def change_x():
    # To modify a global variable, we MUST use the 'global' keyword
    global x
    x = 200
    print(f"Changed global x to: {x}")

myfunc()
change_x()
print(f"Global x after function call: {x}")