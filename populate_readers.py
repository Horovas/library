import psycopg2
from faker import Faker
from credentials import server, database, login, password, port


conn = psycopg2.connect(
    host=server, database=database, user=login, password=password, port=port
)
c = conn.cursor()


fake = Faker("ru_RU") # ru_RU, en_US
reader_number = 800


def populate_db():
    reader_data = []

    for i in range(reader_number):
        
        reader_data.append( 
            (
                fake.name(),
                fake.date_time(),
                fake.random_int(min=1, max=5),
            ),
        )

    # print(reader_data)

    insert_query = """
        INSERT INTO readers
            (name, registration_date, status) 
            VALUES (%s, %s, %s)
    """

    c.executemany(insert_query, reader_data)
    conn.commit()


if __name__ == "__main__":
    populate_db()
