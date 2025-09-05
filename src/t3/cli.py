import os
import things
import click
import tempfile
import subprocess
import urllib.parse
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

@cli.command()
def add():
    title: str = ''
    notes: str = ''
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(b'title: ')
        tmp.flush()
        tmp.seek(0)
        editor = os.environ.get('EDITOR', 'vim')
        if editor == 'emacs':
            subprocess.run([editor, tmp.name, '--eval', '(goto-char (point-max))'], check=True)
        else:
            subprocess.run([editor, tmp.name], check=True)
        headers = True
        for line in tmp:
            line = line.decode()
            if line[0] == '#':
                continue
            if headers:
                if line.isspace():
                    headers = False
                    continue
                else:
                    print(line)
                    (name, value) = line.split(':', 1)
                    if name == 'title':
                        title = value.strip()
            else:
                notes = f"{notes}\n{line}"
                pass
    if title:
        u = url(command="add", title=title, notes=notes)
        print(u)
        os.system(f"open '{u}'")

def url(uuid=None, command="show", **query_parameters) -> str:
    """
    Return a things:///<command>?<query> url.

    For details about available commands and their parameters
    consult the Things URL Scheme documentation
    [here](https://culturedcode.com/things/help/url-scheme/).

    Parameters
    ----------
    uuid : str or None, optional
        A valid uuid of any Things object.
        If `None`, then 'id' is not added as a parameter unless
        specified in `query_parameters`.

    command : str, default 'show'
        A valid command name.

    **query_parameters:
        Additional URL query parameters.

    Examples
    --------
    >>> things.url('6Hf2qWBjWhq7B1xszwdo34')
    'things:///show?id=6Hf2qWBjWhq7B1xszwdo34'
    >>> things.url(command='update', uuid='6Hf2qWBjWhq7B1xszwdo34', title='new title')
    'things:///update?id=6Hf2qWBjWhq7B1xszwdo34&title=new%20title&auth-token=vKkylosuSuGwxrz7qcklOw'
    >>> things.url(command='add', title='new task', when='in 3 days', deadline='in 6 days')
    'things:///add?title=new%20task&when=in%203%20days&deadline=in%206%20days'
    >>> query_params = {'title': 'test title', 'list-id': 'ba5d1237-1dfa-4ab8-826b-7c27b517f29d'}
    >>> things.url(command="add", **query_params)
    'things:///add?title=test%20title&list-id=ba5d1237-1dfa-4ab8-826b-7c27b517f29d'
    """
    if uuid is not None:
        query_parameters = {"id": uuid, **query_parameters}

    # authenticate if needed
    if command in ("update", "update-project"):
        auth_token = query_parameters["auth-token"] = token()
        if not auth_token:
            raise ValueError("Things URL scheme authentication token could not be read")

    query_string = urllib.parse.urlencode(
        query_parameters, quote_via=urllib.parse.quote
    )

    return f"things:///{command}?{query_string}"

def token():
    return "hello"

if __name__ == "__main__":
    cli()
