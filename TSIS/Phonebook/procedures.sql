-- 1. Вставить или обновить (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_last_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    -- Проверяем связку Имя + Фамилия
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name AND last_name = p_last_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name AND last_name = p_last_name;
    ELSE
        INSERT INTO phonebook(name, last_name, phone) VALUES(p_name, p_last_name, p_phone);
    END IF;
END;
$$;

-- 2. Массовая вставка с проверкой через RegEx
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names VARCHAR[], p_last_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Проверка:
        -- ^\+?     -> может начинаться с одного плюса
        -- [0-9]    -> дальше только цифры
        -- {10,15}  -> общее количество цифр от 10 до 15
        -- $        -> конец строки
        IF p_phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            INSERT INTO phonebook(name, last_name, phone) 
            VALUES(p_names[i], p_last_names[i], p_phones[i])
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            -- Теперь мы реально будем видеть в консоли, какой номер "кривой"
            RAISE NOTICE 'Skipping invalid phone format: %', p_phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Удаление (ищет по имени, фамилии или телефону)
CREATE OR REPLACE PROCEDURE delete_contact_by_id(p_id INT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook WHERE id = p_id;
    IF FOUND THEN
        RAISE NOTICE 'Контакт с ID % успешно удален.', p_id;
    ELSE
        RAISE NOTICE 'Ошибка: Контакт с ID % не найден.', p_id;
    END IF;
END;
$$;