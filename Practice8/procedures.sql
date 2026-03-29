-- 1. Вставить или обновить (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Массовая вставка с валидацией номера (длина > 10)
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Если номер длиннее 10 символов - вставляем
        IF length(p_phones[i]) >= 10 THEN
            INSERT INTO phonebook(name, phone) VALUES(p_names[i], p_phones[i])
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            RAISE NOTICE 'Skipping invalid phone: %', p_phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact_v2(p_target VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook WHERE name = p_target OR phone = p_target;
END;
$$;