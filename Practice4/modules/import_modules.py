import my_module as mx

# 1. Accessing variables and functions via alias
age = mx.person1["age"]
print(f"Age from module: {age}")
mx.greeting("Ahmad")

# 2. Using dir() to list all defined names in a module
import platform
print(f"Functions in platform module: {dir(platform)[:5]}...") 

# 3. Import from Module
from my_module import person1
print(f"Direct access to person1 first_name: {person1['first_name']}")

# --- THE __name__ TRICK ---
print(f"\nCurrently running file: {__name__}")
print(f"Imported module name: {mx.__name__}")

if __name__ == "__main__":
    print("This script (import_modules.py) is the main entry point!")