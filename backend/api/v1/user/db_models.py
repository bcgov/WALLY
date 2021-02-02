from sqlalchemy import String, Column, ARRAY, TEXT
from api.db.base_class import Base


from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'public'}

    user_uuid = Column(UUID(), primary_key=True,
                       comment='The keycloak auth user uuid that is returned after oauth login. '
                               'We use this table to keep track of user specific information.')
    user_idir = Column(String, primary_key=True,
                       comment='The user\'s IDIR')


class UserMapLayer(Base):
    __tablename__ = 'user_map_layer'
    __table_args__ = {'schema': 'public'}

    # Note: this is a keycloak string id, not a real 128-bit UUID
    user_idir = Column(String, primary_key=True,
                       comment='The user\'s IDIR')
    default_map_layers = Column(ARRAY(TEXT),
                                comment='Default map layer names that the user last used.')
