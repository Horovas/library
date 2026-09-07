
--Для использования типа данных ISBN нужно предварительно активировать расширение в PostgreSQL командой:
CREATE EXTENSION IF NOT EXISTS isn;


--Создаём словарь статусов книги
CREATE TABLE book_status(
	id SERIAL PRIMARY KEY,
	name TEXT,
	description TEXT
);


-- Создаём таблицу книг
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_year INT,
    isbn_code ISBN,
    status INT,
    CONSTRAINT fk_book_status 
    FOREIGN KEY (status) REFERENCES book_status (id)
);


-- Создаём словарь статусов читателей
CREATE TABLE reader_status(
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT
);


-- Создаём таблицу читателей
CREATE TABLE readers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    registration_date datetime,
    status INT,
    description TEXT
    CONSTRAINT fk_reader_status 
    FOREIGN KEY (status) REFERENCES reader_status (id)
);


-- Создаём таблицу смены статуса пользователя
CREATE TABLE reader_status_log (
    id SERIAL PRIMARY KEY,
    reader_id INT NOT NULL REFERENCES readers(id),
    old_status INT,
    new_status INT NOT NULL,
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    meta JSONB
--    CONSTRAINT fk_reader
--    FOREIGN KEY (reader_id) REFERENCES readers (id)
);

CREATE INDEX idx_reader_status_log ON reader_status_log(reader_id);

-- функция
-- DROP FUNCTION public.log_reader_status_change();
CREATE OR REPLACE FUNCTION log_reader_status_change()
RETURNS TRIGGER AS $$
BEGIN

    IF (TG_OP = 'INSERT') OR (OLD.status IS DISTINCT FROM NEW.status) THEN
        
        INSERT INTO reader_status_log (
            reader_id, 
            old_status, 
            new_status, 
            meta
        )
        VALUES (
            NEW.id,
            CASE WHEN TG_OP = 'INSERT' THEN NULL ELSE OLD.status END,
            NEW.status,
            jsonb_build_object(
                'trigger_operation', TG_OP,
                'db_user', CURRENT_USER
            )
        );
        
    END IF;
    
    -- Triggers must return NEW for AFTER/BEFORE UPDATE operations to succeed
    RETURN NEW; 
END;
$$ LANGUAGE plpgsql;


-- specialized JSON operators (->, ->>, #>, #>>, and @>) 

-- сам тригер
CREATE TRIGGER trg_readers_status_changed
    AFTER INSERT OR UPDATE OF status
    ON readers
    FOR EACH ROW
    EXECUTE FUNCTION log_reader_status_change();


