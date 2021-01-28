from sqlalchemy import String, Column, DateTime, ARRAY, TEXT
from sqlalchemy.ext.declarative import declarative_base
from api.db.base_class import BaseTable
from sqlalchemy.dialects.postgresql import UUID


class Base(object):
    __table_args__ = {'schema': 'metadata'}

    create_date = Column(
        DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')


Base = declarative_base(cls=Base, metadata=BaseTable.metadata)


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'public'}

    # Note: this is a keycloak string id, not a real 128-bit UUID
    uuid = Column(String, primary_key=True,
                  comment='The keycloak auth user id that is returned after oauth login. '
                  'We use this table to keep track of user specific information.')
    default_map_layers = Column(ARRAY(TEXT),
                  comment='Default map layer names that the user last used.')
