import pytest

from app.tests.utils.utils import get_server_api


@pytest.fixture(scope="module")
def server_api():
    return get_server_api()
