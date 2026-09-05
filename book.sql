

--Создаём словарь статусов книги, который примерно отражает возможные положения книги в процессе её использования
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




