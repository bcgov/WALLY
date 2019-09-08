from sqlalchemy import Column, Text, Table
from geoalchemy2 import Geometry
from app.db.base_class import BaseTable


geocode = Table("geocode_lookup", BaseTable.metadata,
                Column("center", Text),
                Column("primary_id", Text),
                Column("kind", Text)
                )
