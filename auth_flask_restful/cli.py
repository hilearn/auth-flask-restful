import secrets
import click
from flask.cli import AppGroup
from .auth_models import ApiUser, authdb


apiuser_cli = AppGroup('apiusers')


@apiuser_cli.command('create')
@click.argument('email')
@click.argument('description')
def create_user(email, description):
    new_user = ApiUser(email=email,
                       description=description,
                       token=secrets.token_urlsafe(42))
    authdb.session.add(new_user)
    authdb.session.commit()

    print(f'Created new user {new_user}')
    print(f'token is: {new_user.token}')
