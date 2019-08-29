from starlette.testclient import TestClient
from main import app


def test_health_check():
    """ test that the health check handler returns a 200 OK status """
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
