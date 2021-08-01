from rich import console
from rich.console import Console
from rich.traceback import install
from rich.console import Console
from rich.theme import Theme
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel
from rich.color import Color
from rich import pretty, print, inspect
from rich.text import Text
from rich.progress import track
# rich documentation: https://rich.readthedocs.io/en/latest/

class RichText:

    @classmethod
    def dev_test(cls):
        # RichText.table()
        # print(['hello', True])
        # print(Panel.fit('[bold yellow]Hi, I am joker[/]', border_style='red'))
        # color = Color.parse('red')
        # inspect(color)
        # RichText.console.print([1,2,3])
        # RichText.console.print('[blue underline]Look like a link[/]')
        # RichText.console.print(locals())
        # RichText.console.print('foo', style = 'underline link https://www.baidu.com')
        # RichText.console.log('Hello world', log_locals=True)
        # RichText.console.out('Locals', locals())
        # RichText.console.rule('[bold red]Chapter 2', align='center')
        # with RichText.console.status("Workings....", spinner='runner'):
        #     i = 0
        #     while i < 100000000:
        #         i = i + 1

        # RichText.console.input('What is [i]your[/] [bold red]name[/]? :smiley: ')
        # RichText.console.save_html('/Users/joker/Desktop/console.html')
        # RichText.console.print(Panel(Text('Hello', justify='right')))
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
        pretty.install()

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
    def table(cls, title, table_data, caption = None):
        t = Table(
            title = title,
            title_style = 'green bold',
            caption = caption,
            caption_style = 'gray',
            highlight = True,
            show_lines = True,
            show_header = False)
        for row in table_data:
            t.add_row(*row)
        RichText.console.print(t)