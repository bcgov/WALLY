import random
import string

import requests

from app.core import config


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_server_api():
    server_name = f"http://{config.SERVER_NAME}"
    return server_name
