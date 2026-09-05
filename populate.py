import psycopg2
from faker import Faker
from credentials import server, database, login, password, port


conn = psycopg2.connect(
    host=server, database=database, user=login, password=password, port=port
)
c = conn.cursor()


fake = Faker("ru_RU") # ru_RU, en_US
book_number = 100000


def populate_db():
    book_data = []

    for i in range(book_number):
        isbn = fake.isbn10(separator="") if i % 2 == 0 else fake.isbn13(separator="")

        book_data.append(
            (
                fake.catch_phrase(),
                fake.name(),
                fake.random_int(min=1900, max=2026),
                isbn,
                fake.random_int(min=1, max=6),
            ),
        )

    # print(book_data)

    insert_query = """
        INSERT INTO postgres.public.books 
            (title, author, published_year, isbn_code, status) 
            VALUES ( %s, %s, %s, %s, %s)
    """

    c.executemany(insert_query, book_data)
    conn.commit()


if __name__ == "__main__":
    populate_db()
