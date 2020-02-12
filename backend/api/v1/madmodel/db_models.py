# from sqlalchemy import Integer, String, Column, DateTime, JSON, Text, ForeignKey, ARRAY, text
# from sqlalchemy.orm import relationship, backref
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.dialects.postgresql import ARRAY, TEXT
# from api.db.base_class import BaseTable

# # Custom Base Class


# class Base(object):
#     __table_args__ = {'schema': 'modeling'}

#     create_user = Column(
#         String(100), comment='The user who created this record in the database.')
#     create_date = Column(
#         DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
#     update_user = Column(
#         String(100), comment='The user who last updated this record in the database.')
#     update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
#                                            'It will be the same as the create_date until the record is first '
#                                            'updated after creation.')
#     effective_date = Column(
#         DateTime, comment='The date and time that the code became valid and could be used.')
#     expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
#                                            'should not be used.')


# Base = declarative_base(cls=Base, metadata=BaseTable.metadata)


# # Data Storage Tables
# class ModelOutputTypeCode(Base):
#     __tablename__ = 'model_output_type_code'

#     data_store_id = Column(Integer, primary_key=True)

#     name = Column(String, comment='data store detail name', index=True)
#     description = Column(
#         String, comment='explanation behind data store and use case')
#     time_relevance = Column(
#         Integer, comment='how long before this data store becomes stale, measured in DAYS')
#     last_updated = Column(
#         DateTime, comment='last time data store was updated from sources')

#     data_sources = relationship("DataSource")