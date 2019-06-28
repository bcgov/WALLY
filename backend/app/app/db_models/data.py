from geoalchemy2.types import Geometry
from sqlalchemy import Column, Integer, Text, UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.base_class import Base


class DataSet(Base):
    """
    DataSet is a data set within a channel. For example, a Data record could represent
    the data from a single weather station within a larger Channel of similar data.
    """

    __tablename__ = 'dataset'

    id = Column('dataset_guid', UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(Text, index=True)

    # external web, API, etc
    type = Column('dataset_type', Text, index=True)

    # URI where data can be automatically retrieved (for display in graphs, etc)
    api_uri = Column(Text)

    # URI where users can go to see more information, view data that is not stored
    # in-app, or check sources
    web_uri = Column(Text)

    # Coordinates indicates where the data was collected.
    # If data is applicable to a defined region, that information should
    # be stored in another column.
    coordinates = Column(Geometry('POINT', 4326))
