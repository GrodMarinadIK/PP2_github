# phonebook.py
# TSIS 1 — Extended PhoneBook
# Builds on Practice 7–8 (CRUD, CSV, upsert, bulk-insert, paginated query, delete).
# New features: groups, email, birthday, multi-phone, JSON export/import, advanced search.

import os
import csv
import json
import time
from datetime import datetime, date
from connect import get_connection

file_path = os.path.dirname(__file__)
contacts_csv = os.path.join(file_path, "contacts.csv")
print(f"Using CSV file: {contacts_csv}")
json_export_path = os.path.join(file_path, "contacts_export.json")
print(f"Using JSON export file: {json_export_path}")

# ─────────────────────────────────────────────
# HELPER UTILITIES
# ─────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")

def print_separator(label=""):
    width = 60
    if label:
        side = (width - len(label) - 2) // 2
        print("=" * side + f" {label} " + "=" * (width - side - len(label) - 2))
    else:
        print("=" * width)

def print_contact_row(row, show_index=None):
    """Prints a single contact row (tuple from DB function)."""
    # row: (id, name, last_name, email, birthday, grp, phones)
    idx_label = f"[{show_index}] " if show_index is not None else ""
    grp     = row[5] or "—"
    phones  = row[6] or "—"
    email   = row[3] or "—"
    bday    = str(row[4]) if row[4] else "—"
    print(f"{idx_label}ID:{row[0]:>4} | {row[1]} {row[2]}")
    print(f"       📧 {email}  🎂 {bday}  👥 {grp}")
    print(f"       📞 {phones}")
    print()

def serialize_contact(row):
    """Converts DB row to a JSON-friendly dict."""
    return {
        "id":        row[0],
        "name":      row[1],
        "last_name": row[2],
        "email":     row[3],
        "birthday":  str(row[4]) if row[4] else None,
        "group":     row[5],
        "phones":    row[6],
    }

def ask_date(prompt):
    """Prompts for a date in YYYY-MM-DD format, returns string or None."""
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        print("  ⚠  Invalid date format. Skipping birthday.")
        return None

def choose_group(conn):
    """Lists available groups and lets user pick one. Returns group_id or None."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM groups ORDER BY id")
        groups = cur.fetchall()

    print("\nAvailable groups:")
    for g in groups:
        print(f"  {g[0]}. {g[1]}")
    print("  0. No group / skip")

    try:
        choice = int(input("Select group number: "))
        if choice == 0:
            return None
        ids = [g[0] for g in groups]
        if choice in ids:
            return choice
        print("  ⚠  Invalid choice — no group assigned.")
        return None
    except ValueError:
        return None

# ─────────────────────────────────────────────
# SEARCH & DISPLAY (uses new search_contacts function)
# ─────────────────────────────────────────────

def search_contacts(pattern):
    conn = get_connection()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        rows = cur.fetchall()
    conn.close()

    print_separator(f"Search: '{pattern}'")
    if not rows:
        print("  Nothing found.")
    for row in rows:
        print_contact_row(row)
    print(f"  Total found: {len(rows)}")

def search_by_email(pattern):
    conn = get_connection()
    if not conn:
        return
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        rows = cur.fetchall()
    conn.close()

    print_separator(f"Email search: '{pattern}'")
    if not rows:
        print("  Nothing found.")
    for row in rows:
        print_contact_row(row)
    print(f"  Total found: {len(rows)}")

# ─────────────────────────────────────────────
# PAGINATED VIEW with keyboard navigation
# ─────────────────────────────────────────────

def view_contacts_paged(sort_by="name"):
    LIMIT = 5
    offset = 0
    conn = get_connection()
    if not conn:
        return

    while True:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM get_contacts_paginated_full(%s, %s, %s)",
                (LIMIT, offset, sort_by)
            )
            rows = cur.fetchall()

        clear()
        print_separator(f"Contacts (sort: {sort_by}, page {offset // LIMIT + 1})")
        if not rows:
            print("  No contacts on this page.")
        else:
            for row in rows:
                print_contact_row(row)

        print(f"  [n] Next   [p] Prev   [q] Quit")
        nav = input("  → ").strip().lower()

        if nav == 'n':
            if len(rows) == LIMIT:
                offset += LIMIT
            else:
                print("  Already on last page.")
                time.sleep(1)
        elif nav == 'p':
            if offset >= LIMIT:
                offset -= LIMIT
            else:
                print("  Already on first page.")
                time.sleep(1)
        elif nav == 'q':
            break

    conn.close()

# ─────────────────────────────────────────────
# FILTER BY GROUP
# ─────────────────────────────────────────────

def filter_by_group():
    conn = get_connection()
    if not conn:
        return

    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM groups ORDER BY id")
        groups = cur.fetchall()

    print_separator("Filter by Group")
    group_map = {} # Словарь для быстрого поиска: {id: name}
    for g in groups:
        print(f"  {g[0]}. {g[1]}")
        group_map[str(g[0])] = g[1]

    choice = input("Enter group number or name: ").strip()

    # Если ввели число, которое есть в списке — берем имя группы
    if choice in group_map:
        group_name = group_map[choice]
    else:
        group_name = choice # Иначе ищем по тексту, как раньше

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM get_contacts_by_group(%s)", (group_name,))
        rows = cur.fetchall()
    conn.close()

    print_separator(f"Results for: '{group_name}'")
    if not rows:
        print("  No contacts in this group.")
    for row in rows:
        # row: (id, name, last_name, email, birthday, phones)  — no grp column here
        print(f"  ID:{row[0]:>4} | {row[1]} {row[2]}")
        print(f"         📧 {row[3] or '—'}  🎂 {str(row[4]) if row[4] else '—'}")
        print(f"         📞 {row[5] or '—'}")
        print()
    print(f"  Total: {len(rows)}")

# ─────────────────────────────────────────────
# ADD CONTACT (upsert via new contacts table)
# ─────────────────────────────────────────────

def add_contact():
    conn = get_connection()
    if not conn:
        return

    print_separator("Add / Update Contact")
    name      = input("First name : ").strip()
    last_name = input("Last name  : ").strip()
    email     = input("Email      : ").strip() or None
    birthday  = ask_date("Birthday (YYYY-MM-DD, or Enter to skip): ")
    group_id  = choose_group(conn)

    # Phone(s)
    phones = []
    print("\nAdd phone numbers (leave blank to stop):")
    while True:
        phone = input("  Phone: ").strip()
        if not phone:
            break
        ptype = input("  Type [mobile/home/work] (default: mobile): ").strip() or "mobile"
        if ptype not in ("mobile", "home", "work"):
            ptype = "mobile"
        phones.append((phone, ptype))

    with conn.cursor() as cur:
        # Check if contact already exists (same name)
        cur.execute(
            "SELECT id FROM contacts WHERE name = %s AND last_name = %s",
            (name, last_name)
        )
        existing = cur.fetchone()

        if existing:
            contact_id = existing[0]
            cur.execute(
                "UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
                (email, birthday, group_id, contact_id)
            )
            print(f"\n  ✅ Updated existing contact ID {contact_id}.")
        else:
            cur.execute(
                "INSERT INTO contacts (name, last_name, email, birthday, group_id) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (name, last_name, email, birthday, group_id)
            )
            contact_id = cur.fetchone()[0]
            print(f"\n  ✅ Added new contact ID {contact_id}.")

        # Insert phones
        for phone, ptype in phones:
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s) "
                "ON CONFLICT (contact_id, phone) DO NOTHING",
                (contact_id, phone, ptype)
            )

        conn.commit()

    conn.close()

# ─────────────────────────────────────────────
# ADD PHONE to existing contact (calls procedure)
# ─────────────────────────────────────────────

def add_phone_to_contact():
    print_separator("Add Phone to Contact")
    name  = input("Contact name or last name: ").strip()
    phone = input("Phone number: ").strip()
    ptype = input("Type [mobile/home/work] (default: mobile): ").strip() or "mobile"
    if ptype not in ("mobile", "home", "work"):
        ptype = "mobile"

    conn = get_connection()
    if not conn:
        return

    with conn.cursor() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        for notice in conn.notices:
            print(" ", notice.strip())

    conn.close()

# ─────────────────────────────────────────────
# MOVE CONTACT TO GROUP (calls procedure)
# ─────────────────────────────────────────────

def move_contact_to_group():
    print_separator("Move Contact to Group")
    name  = input("Contact name or last name: ").strip()
    group = input("Group name: ").strip()

    conn = get_connection()
    if not conn:
        return

    with conn.cursor() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        for notice in conn.notices:
            print(" ", notice.strip())

    conn.close()

# ─────────────────────────────────────────────
# DELETE CONTACT (smart — search first, then pick ID)
# ─────────────────────────────────────────────

def delete_contact():
    print_separator("Delete Contact")
    target = input("Enter name, last name, or phone to search: ").strip()

    conn = get_connection()
    if not conn:
        return

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (target,))
        rows = cur.fetchall()

    if not rows:
        print(f"  Nothing found for '{target}'.")
        conn.close()
        return

    print(f"\nFound {len(rows)} contact(s):")
    for row in rows:
        print_contact_row(row)

    try:
        choice = int(input("Enter ID to delete (0 to cancel): "))
        if choice == 0:
            print("  Cancelled.")
        else:
            found_ids = [r[0] for r in rows]
            if choice in found_ids:
                with conn.cursor() as cur:
                    cur.execute("CALL delete_contact_by_id(%s)", (choice,))
                    conn.commit()
                    for notice in conn.notices:
                        print(" ", notice.strip())
            else:
                print("  ⚠  ID not in search results. Cancelled.")
    except ValueError:
        print("  ⚠  Invalid input.")

    conn.close()

# ─────────────────────────────────────────────
# CSV IMPORT (extended: email, birthday, group, phone type)
# ─────────────────────────────────────────────

def import_from_csv():
    """
    Expected CSV columns:
      name, last_name, phone, [phone_type], [email], [birthday], [group]
    Minimal required: name, last_name, phone
    """
    print_separator("Import from CSV")
    csv_path = input("Path to CSV file (Enter = contacts.csv): ").strip() or contacts_csv

    if not os.path.exists(csv_path):
        print(f"  ⚠  File not found: {csv_path}")
        return

    conn = get_connection()
    if not conn:
        return

    inserted = skipped = 0

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name      = row.get('name', '').strip()
            last_name = row.get('last_name', '').strip()
            phone     = row.get('phone', '').strip()
            ptype     = row.get('phone_type', 'mobile').strip() or 'mobile'
            email     = row.get('email', '').strip() or None
            birthday  = row.get('birthday', '').strip() or None
            group_name= row.get('group', '').strip() or None

            if not name or not phone:
                skipped += 1
                continue

            if ptype not in ('mobile', 'home', 'work'):
                ptype = 'mobile'

            with conn.cursor() as cur:
                # Resolve group
                group_id = None
                if group_name:
                    cur.execute("SELECT id FROM groups WHERE name ILIKE %s", (group_name,))
                    g = cur.fetchone()
                    if g:
                        group_id = g[0]
                    else:
                        cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                        group_id = cur.fetchone()[0]

                # Upsert contact
                cur.execute(
                    "SELECT id FROM contacts WHERE name=%s AND last_name=%s",
                    (name, last_name)
                )
                existing = cur.fetchone()
                if existing:
                    contact_id = existing[0]
                else:
                    cur.execute(
                        "INSERT INTO contacts (name, last_name, email, birthday, group_id) "
                        "VALUES (%s,%s,%s,%s,%s) RETURNING id",
                        (name, last_name, email, birthday, group_id)
                    )
                    contact_id = cur.fetchone()[0]

                # Insert phone (validate format)
                import re
                if re.match(r'^\+?[0-9]{10,15}$', phone):
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) "
                        "VALUES (%s,%s,%s) ON CONFLICT (contact_id, phone) DO NOTHING",
                        (contact_id, phone, ptype)
                    )
                    inserted += 1
                else:
                    print(f"  ⚠  Skipping invalid phone '{phone}' for {name} {last_name}")
                    skipped += 1

        conn.commit()

    conn.close()
    print(f"\n  ✅ Done. Inserted/updated: {inserted}  Skipped: {skipped}")

# ─────────────────────────────────────────────
# JSON EXPORT
# ─────────────────────────────────────────────

def export_to_json():
    print_separator("Export to JSON")
    out_path = input("Output file (Enter = contacts_export.json): ").strip() or json_export_path

    conn = get_connection()
    if not conn:
        return

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM get_contacts_paginated_full(10000, 0, 'name')")
        rows = cur.fetchall()

    conn.close()

    data = [serialize_contact(row) for row in rows]

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n  ✅ Exported {len(data)} contacts to '{out_path}'.")

# ─────────────────────────────────────────────
# JSON IMPORT (with duplicate handling)
# ─────────────────────────────────────────────

def import_from_json():
    print_separator("Import from JSON")
    in_path = input("JSON file to import (Enter = contacts_export.json): ").strip() or json_export_path

    if not os.path.exists(in_path):
        print(f"  ⚠  File not found: {in_path}")
        return

    with open(in_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    conn = get_connection()
    if not conn:
        return

    imported = skipped = overwritten = 0

    for entry in data:
        name      = entry.get("name", "").strip()
        last_name = entry.get("last_name", "").strip()
        email     = entry.get("email")
        birthday  = entry.get("birthday")
        group_name= entry.get("group")
        phones_raw= entry.get("phones", "")  # "07011234 (mobile), 07099 (home)"

        if not name:
            skipped += 1
            continue

        with conn.cursor() as cur:
            # Resolve group
            group_id = None
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name ILIKE %s", (group_name,))
                g = cur.fetchone()
                if g:
                    group_id = g[0]
                else:
                    cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                    group_id = cur.fetchone()[0]

            # Check duplicate
            cur.execute(
                "SELECT id FROM contacts WHERE name=%s AND last_name=%s",
                (name, last_name)
            )
            existing = cur.fetchone()

            if existing:
                print(f"\n  ⚠  Duplicate: {name} {last_name}")
                action = input("    (s)kip / (o)verwrite? ").strip().lower()
                if action == 'o':
                    contact_id = existing[0]
                    cur.execute(
                        "UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE id=%s",
                        (email, birthday, group_id, contact_id)
                    )
                    overwritten += 1
                else:
                    skipped += 1
                    continue
            else:
                cur.execute(
                    "INSERT INTO contacts (name, last_name, email, birthday, group_id) "
                    "VALUES (%s,%s,%s,%s,%s) RETURNING id",
                    (name, last_name, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]
                imported += 1

            # Parse and insert phones from the aggregated string
            if phones_raw:
                import re
                # Each entry looks like "number (type)"
                for match in re.finditer(r'([+\d]+)\s*\((\w+)\)', phones_raw):
                    ph_num  = match.group(1)
                    ph_type = match.group(2) if match.group(2) in ('mobile','home','work') else 'mobile'
                    cur.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s) "
                        "ON CONFLICT (contact_id, phone) DO NOTHING",
                        (contact_id, ph_num, ph_type)
                    )

        conn.commit()

    conn.close()
    print(f"\n  ✅ Done. New: {imported}  Overwritten: {overwritten}  Skipped: {skipped}")

# ─────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────

def main_menu():
    print_separator("PHONEBOOK  TSIS 1")
    print("  VIEW & SEARCH")
    print("  1. 📖 Browse contacts (paged)")
    print("  2. 🔍 Search by name / phone / email")
    print("  3. 📧 Search by email")
    print("  4. 👥 Filter by group")
    print()
    print("  MANAGE CONTACTS")
    print("  5. ➕ Add / update contact")
    print("  6. 📞 Add phone to contact")
    print("  7. 🔀 Move contact to group")
    print("  8. 🗑  Delete contact")
    print()
    print("  IMPORT / EXPORT")
    print("  9. 📥 Import from CSV")
    print(" 10. 📤 Export to JSON")
    print(" 11. 📥 Import from JSON")
    print()
    print("  0. 🚪 Exit")
    print_separator()
    print(f"Using JSON export file: {json_export_path}")
    print(f"Using CSV file: {contacts_csv}")
    return input("  Choose: ").strip()

def run():
    while True:
        clear()
        choice = main_menu()

        if choice == '1':
            sort_options = {'1': 'name', '2': 'birthday', '3': 'created_at'}
            print("\n  Sort by: [1] Name  [2] Birthday  [3] Date added")
            sort_key = sort_options.get(input("  → ").strip(), 'name')
            view_contacts_paged(sort_by=sort_key)

        elif choice == '2':
            pattern = input("Search query: ").strip()
            search_contacts(pattern)
            pause()

        elif choice == '3':
            pattern = input("Email pattern (e.g. gmail): ").strip()
            search_by_email(pattern)
            pause()

        elif choice == '4':
            filter_by_group()
            pause()

        elif choice == '5':
            add_contact()
            pause()

        elif choice == '6':
            add_phone_to_contact()
            pause()

        elif choice == '7':
            move_contact_to_group()
            pause()

        elif choice == '8':
            delete_contact()
            pause()

        elif choice == '9':
            import_from_csv()
            pause()

        elif choice == '10':
            export_to_json()
            pause()

        elif choice == '11':
            import_from_json()
            pause()

        elif choice == '0':
            print("\n  Goodbye! 👋")
            break

        else:
            print("  ⚠  Unknown command.")
            time.sleep(1)

if __name__ == "__main__":
    run()