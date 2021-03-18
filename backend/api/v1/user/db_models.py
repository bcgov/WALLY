from sqlalchemy import String, Column, ARRAY, TEXT, DateTime
from api.db.base_class import Base
from fastapi import Depends
from api.db.utils import get_db
from sqlalchemy.orm import Session

from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'public'}

    user_uuid = Column(UUID(), primary_key=True,
                       comment='The keycloak auth user uuid that is returned after oauth login. '
                               'We use this table to keep track of user specific information.')
    user_idir = Column(String, comment='The user\'s IDIR')
    # last_login = Column(DateTime, comment='Last time the user has logged in')

    @classmethod
    def get_or_create(cls, db: Session, user_uuid):
        user = db.query(User).get(user_uuid)
        if not user:
            user = cls(user_uuid=user_uuid)
            db.add(user)
            db.commit()

        return user


class UserMapLayer(Base):
    __tablename__ = 'user_map_layer'
    __table_args__ = {'schema': 'public'}

    # Note: this is a keycloak string id, not a real 128-bit UUID
    user_idir = Column(String, primary_key=True,
                       comment='The user\'s IDIR')
    default_map_layers = Column(ARRAY(TEXT),
                                comment='Default map layer names that the user last used.')
