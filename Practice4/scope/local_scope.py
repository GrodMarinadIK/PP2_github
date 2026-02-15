def myfunc():
    # Local scope
    x = 300
    def myinnerfunc():
        # Inner functions can access variables from the local scope of the outer function
        print(f"Accessing x from inner function: {x}")
    
    myinnerfunc()
    print(f"Direct access inside myfunc: {x}")

myfunc()
# print(x) # This would raise a NameError because x is not available outside