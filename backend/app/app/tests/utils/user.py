import requests

from app import crud
from app.core import config
from app.db.session import db_session
from app.models.user import UserCreate
from app.tests.utils.utils import random_lower_string


def create_random_user():
    email = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=email, email=email, password=password)
    user = crud.user.create(db_session=db_session, user_in=user_in)
    return user
