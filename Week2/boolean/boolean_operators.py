# Functions can return a boolean value:
def myfunc():
    return True

print(myfunc())

#
print()  
#

if myfunc():
    print("Hell yeah!")
else:
    print("Nah")
    
#
print()
#

# Built-in functions: isinstance() checks object type
x, y = 301, 23.6
print(isinstance(x, int))
print(isinstance(y, int))
