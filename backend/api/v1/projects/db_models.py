from sqlalchemy import String, Column, DateTime, ARRAY, TEXT, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from api.db.base_class import BaseTable
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from api.v1.user.db_models import User

import uuid


class Base(object):
    __table_args__ = {'schema': 'metadata'}

    create_date = Column(
        DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')


Base = declarative_base(cls=Base, metadata=BaseTable.metadata)


class Project(Base):
    __tablename__ = 'project'
    __table_args__ = {'schema': 'public'}

    project_uuid = Column(UUID(as_uuid=True), 
                          primary_key=True, 
                          default=uuid.uuid4, 
                          unique=True, 
                          comment='primary key id for a project')
    name = Column(String, comment='name of the project')
    description = Column(String, comment='description of the project')
    user_uuid = Column(UUID, ForeignKey(User.user_uuid),
                      comment='User who owns this project')
    children = relationship("ProjectDocument", backref="parent", passive_deletes=True, lazy='joined')


class ProjectDocument(Base):
    __tablename__ = 'project_document'
    __table_args__ = {'schema': 'public'}

    project_document_uuid = Column(UUID(as_uuid=True),
                                   primary_key=True,
                                   default=uuid.uuid4,
                                   unique=True,
                                   comment='primary key uuid for a project')
    s3_path = Column(String, comment='path to document in s3 storage system')
    filename = Column(String, comment='filename of the document')
    project_uuid = Column(UUID, ForeignKey(Project.project_uuid),
                          comment='foreign key to the project this document is associated with')
