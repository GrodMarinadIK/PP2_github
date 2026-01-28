# 2p = ... - not correct (variable can't be started with a digit)
# -var = ... - not correct (no special symbols, except underscore)
# None = ... - not correct (can't be already reserved Python keyword)

b = 235       # x is of type int
b = "Lev"     # x is now of type str
print(b)

a = 10       # a is int type
a = float(a) # a is now of float type
print(a)

x = str(52)    # x will be '52'
y = int(67)    # y will be 67
z = float(21)  # z will be 21.0
print(f"x = {x}, y = {y}, z = {z}")
print("Types of those variables:",  type(x), type(y), type(z))

# Variables in Python are case-sensitive & many var-s to many values
v, V = 7, "Seven"
print(f'v = {v}, V = {V}')

print(y + a) # 77.0

text = "Awesome"

def some_func():
    print("Programming is " + text)
    
some_func() # Programming is Awesome

def some_func2():
    text = "cool"
    print("Programming is " + text) 

some_func2() # Programming is cool

print("Programming is " + text) # Programming is Awesome

def some_func3():
    global text 
    text = "Cool"

some_func3()

print("Programming is " + text) # Programming is Cool
print(text) # Cool
    