-- procedures.sql
-- TSIS 1: New stored procedures and functions
-- Do NOT re-run the Practice 8 procedures (upsert_contact, insert_many_contacts,
-- delete_contact_by_id, get_contacts_by_pattern, get_contacts_paginated).
-- They stay as-is and are NOT duplicated here.

-- ============================================================
-- PROCEDURE 1: add_phone
-- Adds a new phone number to an existing contact by name.
-- ============================================================
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Find contact by first name (could also add last_name param if needed)
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name ILIKE p_contact_name OR last_name ILIKE p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO NOTHING;

    IF FOUND THEN
        RAISE NOTICE 'Phone % (%) added to contact ID %.', p_phone, p_type, v_contact_id;
    ELSE
        RAISE NOTICE 'Phone % already exists for this contact.', p_phone;
    END IF;
END;
$$;

-- ============================================================
-- PROCEDURE 2: move_to_group
-- Moves a contact to a group; creates the group if it doesn't exist.
-- ============================================================
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id   INTEGER;
BEGIN
    -- Find or create the group
    SELECT id INTO v_group_id FROM groups WHERE name ILIKE p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        RAISE NOTICE 'Created new group: %', p_group_name;
    END IF;

    -- Find the contact
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name ILIKE p_contact_name OR last_name ILIKE p_contact_name
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;

    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    RAISE NOTICE 'Contact ID % moved to group "%".', v_contact_id, p_group_name;
END;
$$;

-- ============================================================
-- FUNCTION: search_contacts (extended — replaces Practice 8 version)
-- Searches name, last_name, ALL phones, and email.
-- ============================================================
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id        INT,
    name      VARCHAR,
    last_name VARCHAR,
    email     VARCHAR,
    birthday  DATE,
    grp       VARCHAR,
    phones    TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS grp,
        STRING_AGG(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.type) AS phones
    FROM contacts c
    LEFT JOIN groups g  ON g.id  = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE
        c.name      ILIKE '%' || p_query || '%'
        OR c.last_name ILIKE '%' || p_query || '%'
        OR c.email     ILIKE '%' || p_query || '%'
        OR ph.phone    LIKE  '%' || p_query || '%'
    GROUP BY c.id, c.name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.last_name, c.name;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: get_contacts_by_group
-- Returns all contacts belonging to a group (by group name).
-- ============================================================
CREATE OR REPLACE FUNCTION get_contacts_by_group(p_group_name TEXT)
RETURNS TABLE(
    id        INT,
    name      VARCHAR,
    last_name VARCHAR,
    email     VARCHAR,
    birthday  DATE,
    phones    TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.last_name,
        c.email,
        c.birthday,
        STRING_AGG(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.type) AS phones
    FROM contacts c
    JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    WHERE g.name ILIKE p_group_name
    GROUP BY c.id, c.name, c.last_name, c.email, c.birthday
    ORDER BY c.last_name, c.name;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- FUNCTION: get_contacts_paginated_full (extended pagination)
-- Supports sorting by name, birthday, or created_at.
-- ============================================================
CREATE OR REPLACE FUNCTION get_contacts_paginated_full(
    p_limit     INT,
    p_offset    INT,
    p_sort_by   TEXT DEFAULT 'name'   -- 'name' | 'birthday' | 'created_at'
)
RETURNS TABLE(
    id        INT,
    name      VARCHAR,
    last_name VARCHAR,
    email     VARCHAR,
    birthday  DATE,
    grp       VARCHAR,
    phones    TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.last_name,
        c.email,
        c.birthday,
        g.name AS grp,
        STRING_AGG(ph.phone || ' (' || ph.type || ')', ', ' ORDER BY ph.type) AS phones
    FROM contacts c
    LEFT JOIN groups g  ON g.id  = c.group_id
    LEFT JOIN phones ph ON ph.contact_id = c.id
    GROUP BY c.id, c.name, c.last_name, c.email, c.birthday, g.name, c.created_at
    ORDER BY
        CASE WHEN p_sort_by = 'birthday'    THEN c.birthday::TEXT    END ASC NULLS LAST,
        CASE WHEN p_sort_by = 'created_at'  THEN c.created_at::TEXT  END DESC NULLS LAST,
        c.last_name ASC, c.name ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;