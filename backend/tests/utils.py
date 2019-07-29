from alchemy_mock.mocking import AlchemyMagicMock


def get_mock_session():
    """ returns a mock sqlalchemy session """
    session = AlchemyMagicMock()
    return session
