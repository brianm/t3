import things
import click
from click_default_group import DefaultGroup

@click.group(cls=DefaultGroup, default='today', default_if_no_args=True)
def cli():
    pass

@cli.command()
def all():
    for area in things.areas():
        print(area['title'])
        for todo in things.todos(area = area['uuid']):
            print(f"\t{todo['title']}")

@cli.command()
def today():
    for todo in things.today():
        print(todo['title'])

if __name__ == "__main__":
    cli()
