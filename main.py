import click
from click_shell import make_click_shell
import psycopg2
from credentials import server, database, login, password, port

from books import books_group
from readers import readers_group

# Добавляем pass_context, чтобы функция cli получила объект ctx
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Главная панель управления библиотекой."""
    # Если команда запущена без аргументов (просто python3 main.py),
    # мы вручную создаем и запускаем интерактивную оболочку
    if ctx.invoked_subcommand is None:
        shell = make_click_shell(
            ctx,  # Передаем именно объект контекста, а не функцию!
            prompt='library-cli > ',
            intro='Добро пожаловать в систему управления библиотекой'
        )
        shell.cmdloop()

# Регистрируем подгруппы в главном CLI-интерфейсе
cli.add_command(books_group)
cli.add_command(readers_group)


if __name__ == '__main__':

    cli()