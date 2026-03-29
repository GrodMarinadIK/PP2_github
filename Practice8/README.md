# Practice 8: PostgreSQL Functions & Stored Procedures, Phonebook (Cont.)

### Structure:
```
Practice8/
├── config.py           # (copy from P7)
├── connect.py          # (copy from P7)
├── functions.sql       # CREATE FUNCTION
├── procedures.sql      # CREATE PROCEDURE
├── phonebook.py        # new script with calling CALL/SELECT
└── README.md           
```


### Overview:
This practice extends the PhoneBook application by migrating the core CRUD (Create, Read, Update, Delete) logic from the Python application layer directly into the **PostgreSQL** database using **PL/pgSQL**.

### Key Implementations:
- **Server-Side Logic**: Moved all data manipulations to the database via stored procedures and functions.
- **Upsert Procedure**: Implemented `upsert_contact`, which either inserts a new contact or updates the phone number if the name already exists.
- **Data Validation**: The `insert_many_contacts` procedure includes a validation check; phone numbers shorter than 10 digits (e.g., "123") are ignored to ensure data integrity.
- **Pattern Matching**: Created the `get_contacts_by_pattern` function using `ILIKE`. It successfully retrieves contacts like `Jiwoo`, `Jisu`, and `Beeji` when searching for the pattern "Ji".
- **Pagination**: Implemented a function to query data using `LIMIT` and `OFFSET` for efficient data retrieval.

### Execution Results:
- **Search Pattern ('Ji')**: Successfully retrieved 3 contacts (including substring matches like "Beeji").
- **Validation Check**: User "Engin" with the phone number "123" was correctly rejected by the database logic.
- **Bulk Insert**: Successfully processed multiple records in a single database call using arrays.