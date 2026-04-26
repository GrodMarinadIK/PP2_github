# 📱 PhoneBook: Extended Contact Management (TSIS 1)
A robust contact management system built with Python and PostgreSQL. This project demonstrates advanced relational database design, stored procedures (PL/pgSQL), data migration, and integration with CSV/JSON formats.

### 🚀 Key Features
Relational Schema: Data is normalized into three tables: contacts, phones (1-to-many relationship), and groups.

Advanced DB Logic: Uses PL/pgSQL stored procedures for adding phones, moving contacts between groups, and multi-field pattern searching.

Data Exchange:

JSON: Full export and import of the entire database.

CSV: Smart importer that handles new fields and dynamically creates contact groups.

Improved Console UI:

Paginated View: Navigate through large contact lists using Next and Prev commands.

Smart Filtering: Filter contacts by group (using either ID or Name) and search by email patterns.

Sorting: Order results by Name, Birthday, or the date the contact was added.

### 🛠 Tech Stack
Language: Python 3.10+

Database: PostgreSQL 16

Libraries: psycopg2 (DB Driver)

Documentation: LaTeX (used for academic formatting and project reports)

### 📂 Project Structure
```
TSIS1/
├── phonebook.py           # Main application entry point (UI & Logic)
├── config.py              # Database connection parameters
├── connect.py             # Database connection utility
├── schema.sql             # SQL script for table creation and migration
├── procedures.sql         # SQL script for PL/pgSQL functions and procedures
├── generate_contacts.py   # Script for generating randomized test data
└── contacts.csv           # Source file for initial CSV import
```

### ⚙️ Installation & Setup
#### 1. Database Initialization
Create a PostgreSQL database (e.g., phonebook_db) and execute the following scripts in pgAdmin or via psql:

Run schema.sql first to establish the table structure and constraints.

Run procedures.sql to register all necessary search and management functions.

#### 2. Configuration
Update your database credentials in config.py:

```Python
params = {
    "host": "localhost",
    "database": "phonebook_db",
    "user": "postgres",
    "password": "your_secure_password"
}
```
#### 3. Usage
Run the main script to start the interactive console:

```Bash
python phonebook.py
```

### 🏗 Database Highlights
The system implements referential integrity. For example, the phones table uses ON DELETE CASCADE linked to contacts. This ensures that when a contact is deleted via the delete_contact_by_id procedure, all associated phone numbers are automatically wiped, preventing orphaned data.

👤 Author
Zhanspayev Miruansani (GrodMarinad2k)

First-year Undergraduate at KBTU (Computer Systems and Software)