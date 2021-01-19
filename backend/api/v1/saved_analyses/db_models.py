from sqlalchemy import String, Column, Integer, Numeric, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from api.db.base_class import Base
from api.v1.catalogue.db_models import DisplayCatalogue
from api.v1.user.db_models import User
from api.v1.projects.db_models import Project
from sqlalchemy.dialects.postgresql import UUID
import uuid


class SavedAnalysis(Base):
    __tablename__ = 'saved_analysis'
    __table_args__ = {'schema': 'public'}

    saved_analysis_uuid = Column(UUID(as_uuid=True),
                                 primary_key=True,
                                 default=uuid.uuid4,
                                 unique=True,
                                 comment='Primary key id for a saved analysis')
    name = Column(String, comment='Name of the custom analysis')
    description = Column(String, comment='Description of the analysis')
    geometry = Column(String, comment='Geometry of the analysis')
    feature_type = Column(String, comment='Feature used for the analysis')
    zoom_level = Column(Numeric, comment='Zoom level')
    project_id = Column(Integer, ForeignKey(Project.project_id))
    user_id = Column(String, ForeignKey(User.uuid),
                     comment='foreign key to the user who created this project')
    map_layers = relationship('SavedAnalysisMapLayer')


class SavedAnalysisMapLayer(Base):
    __tablename__ = 'saved_analysis_map_layer'
    __table_args__ = {'schema': 'public'}
    __table_args__ = (
        PrimaryKeyConstraint('saved_analysis_uuid', 'map_layer'),
    )

    saved_analysis_uuid = Column(UUID(as_uuid=True), ForeignKey(SavedAnalysis.saved_analysis_uuid))
    map_layer = Column(String, ForeignKey(DisplayCatalogue.display_data_name),
                       comment='Map layer id')
