import shutil
import os

def backup_file(source_path, destination_path):
    """
    Creates a backup of a file. 
    shutil.copy2 is superior because it copies the file content 
    AND the metadata (creation time, modification time, etc.).
    """
    try:
        shutil.copy2(source_path, destination_path)
        print(f"Backup created: {destination_path}")
    except FileNotFoundError:
        print(f"Error: The source file '{source_path}' does not exist.")
    except PermissionError:
        print("Error: You don't have permission to copy this file.")

def safe_delete_file(filename):
    """
    Deletes a file if it exists. 
    Always check with os.path.exists() to avoid a crash.
    """
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")
    else:
        print(f"Warning: File '{filename}' not found, nothing to delete.")

# Example usage:
# backup_file("log.txt", "log_backup.txt")
# safe_delete_file("temp_data.txt")