import asyncio
import random
from datetime import datetime, timedelta

# import bcrypt
import click
import jwt
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Users
from src.repositories import user_repo

# from src.domain.constants import JWT_SECRET_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


@click.command()
@click.option('--firstname', prompt='First name', help='The first name of the user.')
@click.option('--lastname', prompt='Last name', help='The last name of the user.')
@click.option('--username', prompt='Username', help='The username of the user.')
@click.option('--password', prompt='Password', help='The password of the user.')
@click.option('--phone_number', prompt='Phone number', help='The phone number of the user.')
@click.option('--tg_user_id', prompt='Telegram user ID', help='The Telegram user ID of the user.')
def create_user(firstname, lastname, username, password, phone_number, tg_user_id):
    """Create a new user."""
    new_user = {
        "firstname": firstname,
        "lastname": lastname,
        "username": username,
        "password": get_hashed_password(password),
        "phone_number": phone_number,
        "tg_user_id": tg_user_id
    }
    asyncio.run(user_repo.create(new_user))

    click.echo(f'User {username} created successfully!')


if __name__ == '__main__':

    create_user()
