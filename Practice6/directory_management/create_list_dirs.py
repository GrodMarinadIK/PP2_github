import os

def create_folder_structure(path):
    """
    makedirs creates the whole path. 
    If path is 'data/logs/2026', it creates all folders at once.
    exist_ok=True prevents an error if the folder already exists.
    """
    os.makedirs(path, exist_ok=True)
    print(f"Directory structure '{path}' is ready.")

def list_all_files(path):
    """
    os.listdir returns a list of names of entries in the directory.
    """
    try:
        items = os.listdir(path)
        print(f"Contents of '{path}': {items}")
        return items
    except FileNotFoundError:
        print(f"Error: The directory '{path}' does not exist.")
        return []