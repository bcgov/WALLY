from starlette.testclient import TestClient
from main import wally_api


def test_health_check():
    """ test that the health check handler returns a 200 OK status """
    client = TestClient(wally_api)
    response = client.get('/health')
    assert response.status_code == 200
