import click
import psycopg2
from credentials import server, database, login, password, port


# ==========================================
# 1. КОРНЕВАЯ ГРУППА (Главное меню)
# ==========================================
@click.group()
def cli():
    """Главное меню системы управления библиотекой."""
    pass


# ==========================================
# 2. ГРУППА ПЕРВОГО УРОВНЯ: Книги (books)
# ==========================================
@cli.group(name='books')
def books_group():
    """Работа с книгами."""
    pass

# Доступные методы для КНИГ
@books_group.command(name='add')
@click.option('--title', prompt='Введите название книги', help='Название книги')
@click.option('--author', prompt='Введите автора', help='Имя автора')
@click.option('--year', prompt='Год публикации', type=int, help='Только год издания (4 знака)')
@click.option('--isbn', prompt='ISBN-код (10 символов, последний X)', help='Уникальный код книги ISBN')
@click.option('--status', prompt='Статус', default='1', help='Текущий статус книги')
def add_book(title, author, year, isbn, status):
    """Добавить новую книгу."""
    sql = """
        INSERT INTO lib.books 
            (title, author, published_year, isbn_code, status)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    # Кортеж с данными, собранными из консоли через Click
    book_data = (title, author, year, isbn, status)

    try:
        with psycopg2.connect(f"host={server} dbname={database} user={login} password={password}") as conn:
            with conn.cursor() as cur:
                
                cur.execute(sql, book_data)
                conn.commit()
                
                click.echo(click.style(f"\nКнига '{title}' успешно добавлена!", fg='green', bold=True))
                
    except Exception as e:
        click.echo(click.style(f"\nОшибка при добавлении в БД: {e}", fg='red'), err=True)

    

# python3 main.py books edit 4 --title "Новые промышленные предприятия Московской области"
@books_group.command(name='edit')
@click.argument('book_id', type=int)
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
@books_group.command(name='delete')
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


# ==========================================
# 3. ГРУППА ПЕРВОГО УРОВНЯ: Пользователи (users)
# ==========================================
@cli.group(name='users')
def users_group():
    """Работа с пользователями."""
    pass

# Доступные методы для ПОЛЬЗОВАТЕЛЕЙ
@users_group.command(name='create')
@click.option('--name', prompt='Имя пользователя')
def create_user(name):
    """Создать нового пользователя."""
    click.echo(f"Вызываем SQL: INSERT INTO users... Пользователь: {name}")


if __name__ == '__main__':
    cli()
