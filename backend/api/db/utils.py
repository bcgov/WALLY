from starlette.requests import Request
from api.db.session import Session


def get_db(request: Request):
    """ gets a database session for the current HTTP request """
    return request.state.db


def get_db_session():
    """ get a database session"""
    db = Session()
    try:
        return db
    finally:
        db.close()
