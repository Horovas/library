import psycopg2
import argparse
from faker import Faker
from credentials import server, database, login, password, port


conn = psycopg2.connect(
    host=server, database=database, user=login, password=password, port=port
)
c = conn.cursor()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('id', help='order id here', type=int)
    args = parser.parse_args()

    main(order_id=args.id)