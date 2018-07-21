#!/usr/bin/env python
import click

from .fandogh_client.domain_client import *
from .base_commands import FandoghCommand
from .config import *
from .presenter import present
from .utils import login_required, format_text, TextStyle


@click.group("domain")
def domain():
    """
    Domain management commands
    """
    pass


@click.command("add", cls=FandoghCommand)
@click.option('--name', prompt='domain name', help='your domain name')
@login_required
def add(name):
    """
    Upload project on the server
    """
    token = get_user_config().get('token')
    response = add_domain(name, token)
    click.echo('The domain has been added.')
    click.echo('Now you just need to help us that you have ownership of this domain.')
    click.echo('please add a TXT record with the following key to your name server in order to help us verify your ownership.')
    click.echo('Key:' + format_text(response['verification_key'], TextStyle.OKGREEN))
    click.echo('Once you added the record please run the following command')
    click.echo(format_text('fandogh domain verify --name={}'.format(name), TextStyle.BOLD))


@click.command('list', cls=FandoghCommand)
@login_required
def list():
    """
    List images
    """
    token = get_user_config().get('token')
    table = present(lambda: list_domains(token),
                    renderer='table',
                    headers=['Name', 'Creation Date'],
                    columns=['name', 'created_at'])

    click.echo(table)


@click.command('verify', cls=FandoghCommand)
@click.option('--name', 'name', prompt='Domain name', help='The domain name')
@login_required
def verify(name):
    """
    Verify domain ownership
    """
    token = get_user_config().get('token')
    response = verify_domain(name, token)
    if response['verified']:
        click.echo('Domain {} ownership verified successfully.'.format(name))
    else:
        click.echo('It seems the key is not set correctly in TXT.'.format(name))
        click.echo('please add a TXT record with the following key to your name server in order to help us verify your ownership.')
        click.echo('Key:' + format_text(response['verification_key'], TextStyle.OKGREEN))
        click.echo('Once you added the record please run the following command')
        click.echo(format_text('fandogh domain verify --name={}'.format(name), TextStyle.BOLD))


domain.add_command(add)
domain.add_command(list)
domain.add_command(verify)
