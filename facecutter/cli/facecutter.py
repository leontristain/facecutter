import click

from facecutter import foo


@click.command(help='facecutter')
def cli():
    foo()
