from sqlalchemy import Column, Text, Table, BigInteger
from geoalchemy2 import Geometry
from app.db.base_class import BaseTable


geocode = Table("geocode_lookup", BaseTable.metadata,
                Column("center", Text),
                Column("primary_id", Text),
                Column("name", Text),
                Column("kind", Text),
                Column("tsv", Text)
                )

#
#
parcel = Table("parcel", BaseTable.metadata,
               Column("geom", Geometry('MULTIPOLYGON', 4326)),
               Column("PARCEL_FABRIC_POLY_ID", BigInteger),
               Column("PIN", BigInteger),
               Column("PID", BigInteger),
               Column("PARCEL_NAME", BigInteger),
               Column("PLAN_NUMBER", BigInteger),
               )
