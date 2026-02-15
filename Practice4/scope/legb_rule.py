# LEGB Rule: Local -> Enclosing -> Global -> Built-in

# G: Global scope
x = "global"

def outer():
    # E: Enclosing scope
    x = "enclosing"
    
    def inner():
        # L: Local scope
        x = "local"
        print("L level:", x)
        
        # Note: B (Built-in) is always there, like len(), range(), etc.
        print("B level example (len function):", len(x)) 
    
    inner()
    print("E level:", x)

outer()
print("G level:", x)



# Functions are objects too!
x = print 
x("I am derpy") # This works perfectly!

# You can even check it
print(x is print) # Output: True

# Overriding a built-in function (Chaos Mode)
def print(text):
    # Now 'print' doesn't output anything, it just returns a middle finger
    return "🌪🥰🌪🥰🌪🥰"

# Now if you try to use it:
result = print("Hello") 
x(result)
# Standard print is hidden by your global one
# Nothing appears in console, but 'result' now contains the emoji


# ------------------------------------------------------------------------------------------
'''Scope:
Local (L) — in the current function.

Enclosing (E) — in outer function (matryoshka). Using nonlocal, to change

Global (G) — File level. Using global, to change

Built-in (B) — Already in Python itself (e.g. print, int, abs)
'''