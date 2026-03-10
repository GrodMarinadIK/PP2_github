# file_handling/exercises.py
import os

def run_file_exercise():
    filename = "test.txt"
    
    # 1. Creating a file (if it already existed then rewriting it)
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Hello")
    
    # 2.Append
    with open(filename, "a", encoding="utf-8") as f:
        f.write(" World")
        
    # 3. Reading 
    with open(filename, "r", encoding="utf-8") as f:
        print(f"Content: {f.read()}")
        
    # 4. Deleting
    if os.path.exists(filename):
        os.remove(filename)
        print("File deleted.")

run_file_exercise()