'''
r	    Read-only. Raises I/O error if file doesn't exist.
r+ 	    Read and write. Raises I/O error if the file does not exist.
w       Write-only. Overwrites file if it exists, else creates a new one.
w+ 	    Read and write. Overwrites file or creates new one.
a	    Append-only. Adds data to end. Creates file if it doesn't exist.
a+	    Read and append. Pointer at end. Creates file if it doesn't exist.
rb	    Read in binary mode. File must exist.
rb+	    Read and write in binary mode. File must exist.
wb	    Write in binary. Overwrites or creates new.
wb+	    Read and write in binary. Overwrites or creates new.
ab	    Append in binary. Creates file if not exist.
ab+	    Read and append in binary. Creates file if it does not exist.
x       creating a new file only if it doesn't already exist. Othwrwise, it'll raise a FileExistsError.
'''

def save_data(filename, data):
    """
    'w' mode: The "Destroyer". 
    It deletes EVERYTHING in the file and starts fresh.
    Use this only when you want a brand new start.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"File '{filename}' has been completely overwritten.")

def add_data(filename, extra_data):
    """
    'a' mode: The "Helper".
    It opens the file and just adds to the end.
    The old content stays safe.
    """
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"\n{extra_data}")
    print(f"Appended data to '{filename}'.")

# Example usage:
# save_data("log.txt", "Day 1: Started the project.")
# add_data("log.txt", "Day 2: Added more features.")