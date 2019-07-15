from starlette.requests import Request


def get_db(request: Request):
    """ gets a database session for the current request """
    return request.state.db
