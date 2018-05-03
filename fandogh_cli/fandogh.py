#!/usr/bin/env python
import click

from fandogh_client import create_app, create_version, list_versions, deploy_container
from beautifultable import BeautifulTable


# TODO: better description for state field

@click.group("cli")
def base():
    pass


@click.group("app")
def app():
    pass


@click.group("container")
def container():
    pass


base.add_command(app)
base.add_command(container)


@click.command()
@click.option('--name', prompt='application name', help='your application name')
def init(name):
    response = create_app(name)
    # todo: create .fandogh directory
    click.echo(response)


app.add_command(init)


@click.command()
@click.option('--version', prompt='application version', help='your application version')
def publish(version):
    response = create_version('app1', version)
    click.echo(response)


@click.command()
def versions():
    response = list_versions('app1')
    table = BeautifulTable()
    table.column_headers = ['version', 'state']
    table.row_separator_char = ''
    for item in response:
        table.append_row([item.get('version'), item.get('state')])
    click.echo(table)


@click.command()
@click.option('--version', prompt='application version', help='The application version you want to deploy')
def deploy(version):
    app = 'app1'
    response = deploy_container(app, version)
    click.echo(response)


app.add_command(publish)
app.add_command(versions)
container.add_command(deploy)

if __name__ == '__main__':
    base()