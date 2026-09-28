import click
import psycopg2
from datetime import datetime
from credentials import server, database, login, password, port


# Создаем изолированную группу для работы с читателями
@click.group(name='readers')
def readers_group():
    """Работа с читателями (в отдельном файле)."""
    pass


# Доступные методы для читателей
@readers_group.command(name='add')
@click.option('--name', prompt='Введите имя нового читателя', help='Имя нового читателя')
@click.option('--status', prompt='Статус', default='1', help='Текущий статус "активен"')
def add_reader(name, status):
    """Добавить нового читателя"""
    sql = """
        INSERT INTO lib.readers 
            (name, registration_date, status)
        VALUES (%s, %s, %s)
    """
    
    # Кортеж с данными, собранными из консоли через Click
    reader_data = (name, datetime.now(), status)

    try:
        with psycopg2.connect(f"host={server} dbname={database} user={login} password={password}") as conn:
            with conn.cursor() as cur:
                
                cur.execute(sql, reader_data)
                conn.commit()
                
                click.echo(click.style(f"\nЧитатель '{name}' успешно добавлен!", fg='green', bold=True))
                
    except Exception as e:
        click.echo(click.style(f"\nОшибка при добавлении в БД: {e}", fg='red'), err=True)

    

@readers_group.command(name='edit')
@click.argument('reader_id', type=int)
@click.option('--title', help='Новое название')
def edit_book(book_id, title):
    """Редактировать запись о книге по её ID."""
    sql = f"""
        UPDATE lib.books SET title='{title}' WHERE id={book_id}
    """


    try:
        with psycopg2.connect(f"host={server} dbname={database} user={login} password={password}") as conn:
            with conn.cursor() as cur:
                
                cur.execute(sql)
                conn.commit()
                
                click.echo(click.style(f"\nКнига '{title}' успешно обновлена!", fg='green', bold=True))
                
    except Exception as e:
        click.echo(click.style(f"\nОшибка при обновлении в БД: {e}", fg='red'), err=True)

    # click.echo(f"Вызываем SQL: UPDATE books SET title='{title}' WHERE id={book_id}")



# python3 main.py books delete 501008
@readers_group.command(name='delete')
@click.argument('book_id', type=int)
def delete_book(book_id):
    """Удалить книгу из базы данных."""

    sql = f"""
        DELETE FROM lib.books WHERE id={book_id}
    """

    try:
        with psycopg2.connect(f"host={server} dbname={database} user={login} password={password}") as conn:
            with conn.cursor() as cur:
                
                cur.execute(sql)
                conn.commit()
                
                click.echo(click.style(f"\nКнига '{book_id}' успешно удалена!", fg='green', bold=True))
                
    except Exception as e:
        click.echo(click.style(f"\nОшибка при обновлении в БД: {e}", fg='red'), err=True)

    # click.echo(f"Вызываем SQL: DELETE FROM books WHERE id={book_id}")

