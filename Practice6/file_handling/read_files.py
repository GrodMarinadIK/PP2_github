def read_file_line_by_line(filename):
    """
    Reads a file line-by-line. 
    This is the safest way to read large files 
    without crashing your computer's RAM.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                # .strip() removes the '\n' (newline character) 
                # so your output doesn't have extra blank lines.
                print(line.strip())
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

def read_small_file_all_at_once(filename):
    """
    Reads the entire file into memory. 
    Only use this for small config files or short notes.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

# Usage:
# read_file_line_by_line("data.txt")