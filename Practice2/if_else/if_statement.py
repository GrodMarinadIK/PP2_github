# basic example:
a = 3
b = 24

if b > a:
    print("b is greater than a")

# Important: Indentation!
# Without отступы 'print()' will raise an error
if b > a:
    print('Noice indentation')
    
# Что Python считает за True/False:
# 0, "", None, [], (), {} — это False.
# Все остальное — True.
is_logged_in = True
if is_logged_in: 
    print("Welcome back!")
    
