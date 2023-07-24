from starlette.testclient import TestClient
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

from main import wally_api
from api.db.utils import get_db


def test_health_check():
    """ test that the health check handler returns a 200 OK status """
    db = UnifiedAlchemyMagicMock()
    wally_api.dependency_overrides[get_db] = db

    client = TestClient(wally_api)
    response = client.get('/health')
    assert response.status_code == 200
