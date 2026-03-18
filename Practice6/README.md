## 🔗 Practice 6: Python File Handling and Built-in Functions

General structure for Practice 6:

```
Practice6/
├── builtin_functions/
│   ├── enumerate_zip_examples.py
│   └── map_filter_reduce.py
├── directory_management/
│   ├── create_list_dirs.py
│   └── move_files.py
├── file_handling/
│   ├── copy_delete_files.py 
│   ├── read_files.py
│   └── write_files.py
└── README.md
```


### Helpful information about file-handling:
```
r       Read-only. Raises I/O error if file doesn't exist.
r+      Read and write. Raises I/O error if the file does not exist.
w       Write-only. Overwrites file if it exists, else creates a new one.
w+      Read and write. Overwrites file or creates new one.
a       Append-only. Adds data to end. Creates file if it doesn't exist.
a+      Read and append. Pointer at end. Creates file if it doesn't exist.
rb      Read in binary mode. File must exist.
rb+     Read and write in binary mode. File must exist.
wb      Write in binary. Overwrites or creates new.
wb+     Read and write in binary. Overwrites or creates new.
ab      Append in binary. Creates file if not exist.
ab+     Read and append in binary. Creates file if it does not exist.
x       creating a new file only if it doesn't already exist. Othwrwise, it'll raise a FileExistsError.
```