import os
import shutil

def run_dir_exercise():
    # Get the absolute path of the directory where this script resides
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the destination directory relative to the script's location
    target_dir = os.path.join(script_dir, "projects/docs")
    
    # Create the directory tree; exist_ok=True prevents errors if it already exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Iterate through all items in the script's directory
    for file in os.listdir(script_dir):
        # Filter: check if the file has a .py extension
        if file.endswith(".py"):
            source_path = os.path.join(script_dir, file)
            
            # Construct the full destination path
            destination_path = os.path.join(target_dir, file)
            
            # Copy the file along with its metadata (permissions, timestamps)
            shutil.copy2(source_path, destination_path)
            
            print(f"Successfully copied: {file}")

# Execute the function
run_dir_exercise()