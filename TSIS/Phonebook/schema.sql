-- schema.sql
-- TSIS 1: Extended PhoneBook Schema
-- Run this AFTER your existing phonebook_db is set up.
-- It migrates the old "phonebook" table and creates new structure.

-- ============================================================
-- 1. Create groups table
-- ============================================================
CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Seed default groups
INSERT INTO groups (name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- 2. Create new contacts table (replaces old phonebook)
-- ============================================================
CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    last_name  VARCHAR(100) NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- 3. Migrate existing data from old phonebook table (if it exists)
-- ============================================================
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'phonebook'
    ) THEN
        INSERT INTO contacts (name, last_name)
        SELECT name, last_name FROM phonebook
        ON CONFLICT DO NOTHING;

        RAISE NOTICE 'Migrated data from phonebook table.';
    END IF;
END;
$$;

-- ============================================================
-- 4. Create phones table (1-to-many: one contact -> many phones)
-- ============================================================
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) DEFAULT 'mobile' CHECK (type IN ('home', 'work', 'mobile', 'friend', 'family')), -- Добавил типы
    UNIQUE (contact_id, phone)
);

-- Migrate phones from old phonebook if it exists
DO $$
DECLARE
    rec RECORD;
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'phonebook'
    ) THEN
        FOR rec IN SELECT p.name, p.last_name, p.phone FROM phonebook p LOOP
            INSERT INTO phones (contact_id, phone, type)
            SELECT c.id, rec.phone, 'mobile'
            FROM contacts c
            WHERE c.name = rec.name AND c.last_name = rec.last_name
            LIMIT 1
            ON CONFLICT DO NOTHING;
        END LOOP;
        RAISE NOTICE 'Migrated phones from phonebook table.';
    END IF;
END;
$$;