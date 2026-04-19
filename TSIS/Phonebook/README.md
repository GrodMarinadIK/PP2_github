# PostgreSQL Phonebook Manager
A console-based application for managing contact data with a PostgreSQL backend.

### Features
- **Database Integration**: Advanced interaction using PL/pgSQL procedures and functions.
- **Data Validation**: Phone number verification using Regular Expressions directly in SQL.
- **Bulk Import**: Support for importing contact lists from CSV files.

### Installation & Setup
1. **Database Credentials**: 
   - Locate `config.py.example` in the project folder.
   - Rename it to `config.py`.
   - Update the `params` dictionary with your local PostgreSQL username and password.
2. **Dependencies**: Install the required library:
   ```bash
   pip install psycopg2
   ```
3. **Execution**: Run the main script:
```python
python main.py
```

### Technical Note
The connect.py script is designed to securely import credentials from config.py. For security reasons, the actual config.py file is excluded from this repository via .gitignore.
