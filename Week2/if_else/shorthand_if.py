a = 5
b = 2

# Short Hand If (in one line)
if a > b: print("a is greater than b")

# Short Hand If ... Else (Ternary Operator)
print("A") if a > b else print("B")

# assignment using If Else
bigger = a if a > b else b
print(f"Maximum is {bigger}")

# Example with default value
username = ""
display_name = username if username else "Guest"
print(display_name)