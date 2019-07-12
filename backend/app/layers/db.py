import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, UUID
from sqlalchemy.orm import relationship
from geoalchemy2.types import Geometry

from app.db.base_class import BaseTable


class Publisher(BaseTable):
    """
    Database table representation of a data owner.
    A data owner is an organization or government agency that publishes
    data that our users want to access.
    """
    __tablename__ = "publisher"

    id = Column("publisher_guid", UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4())
    name = Column(String, index=True)
    description = Column(String)


class DataSet(BaseTable):
    """
    DataSet is a set of environmental or hydrology data
    """

    __tablename__ = 'dataset'

    id = Column('dataset_guid', UUID(as_uuid=True),
                primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True)

    # external web, API, etc
    type = Column('dataset_type', String, index=True)

    # URI where data can be automatically retrieved (for display in graphs, etc)
    api_uri = Column(String)

    # URI where users can go to see more information, view data that is not stored
    # in-app, or check sources
    web_uri = Column(String)

    # Coordinates indicates where the data was collected.
    # If data is applicable to a defined region, that information should
    # be stored in another column.
    coordinates = Column(Geometry('POINT', 4326))
