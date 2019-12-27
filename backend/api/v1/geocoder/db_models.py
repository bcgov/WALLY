from sqlalchemy import Column, Text, Table, BigInteger
from geoalchemy2 import Geometry
from api.db.base_class import BaseTable


geocode = Table("geocode_lookup", BaseTable.metadata,
                Column("center", Text),
                Column("primary_id", Text),
                Column("name", Text),
                Column("kind", Text),
                Column("tsv", Text),
                Column("layer", Text)
                )
