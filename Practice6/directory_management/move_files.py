import shutil
import os

def move_my_file(source_file, target_folder):
    """
    Moves a file from one place to another.
    We use os.path.join to build the path correctly for any OS (Win/Linux/Mac).
    """
    # Make sure the target folder exists first
    os.makedirs(target_folder, exist_ok=True)
    
    # Construct the destination path: target_folder + source_file
    destination = os.path.join(target_folder, os.path.basename(source_file))
    
    try:
        shutil.move(source_file, destination)
        print(f"Moved '{source_file}' to '{destination}'")
    except FileNotFoundError:
        print(f"Error: The file '{source_file}' was not found.")