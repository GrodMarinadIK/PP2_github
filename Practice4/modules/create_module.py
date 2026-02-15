# This file demonstrates how to structure a module properly

def main_logic():
    print("This is the main logic of the module.")

# The check below prevents code from running when the file is imported.
# It only runs if you execute THIS file directly.
if __name__ == "__main__":
    print("Module is being run directly")
    main_logic()
else:
    print("Module has been imported by another script")