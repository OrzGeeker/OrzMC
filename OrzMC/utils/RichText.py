from rich import prompt
from rich import console
from rich.console import Console
from rich.traceback import install
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.table import Table

class RichText:

    @classmethod
    def dev_test(cls):
        # RichText.table()
        # exit(0)
        pass

    theme = Theme({
        'info': 'green bold',
        'warning': 'yellow bold',
        'error': 'red bold',
    })

    console = Console(theme=theme)

    @classmethod
    def better_debug(cls):
        install()

    @classmethod
    def warn(cls, text):
        RichText.console.print(text, style='warning')

    @classmethod
    def info(cls, text):
        RichText.console.print(text, style='info')
    
    @classmethod
    def error(cls, text):
        RichText.console.print(text, style='error')

    @classmethod
    def prompt(cls, text, choices=None, default=None):
        return Prompt.ask(text, choices=choices, default=default)

    @classmethod
    def table(cls, title = None):
        t = Table(title = title)
        t.add_column('hello')
        t.add_row('1')
        RichText.console.print(t)
        pass