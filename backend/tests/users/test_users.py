from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from api.v1.user.db_models import User

session = UnifiedAlchemyMagicMock()


class TestUsers:
    def test_get_or_create_non_existent_user(self):
        # User does not exist
        user = User.get_or_create(session, 1)
        assert user.user_uuid == 1

    def test_get_or_create_user_exists(self):
        # User exists
        session.add(User(user_uuid=2, user_idir='test'))
        user = User.get_or_create(session, 2)
        assert user.user_uuid != 1
        assert user.user_uuid == 2



