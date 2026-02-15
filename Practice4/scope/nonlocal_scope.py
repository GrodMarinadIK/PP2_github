def myfunc1():
    x = "Jane"
    
    def myfunc2():
        # The 'nonlocal' keyword makes the variable belong to the outer function (myfunc1)
        nonlocal x
        x = "hello"
        print(f"Inside myfunc2 (nonlocal x): {x}")

    myfunc2()
    return x

print(f"Result from myfunc1: {myfunc1()}")