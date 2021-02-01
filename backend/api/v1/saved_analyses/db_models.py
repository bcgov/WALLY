from sqlalchemy import String, Column, Integer, Numeric, ForeignKey, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship, validates
from api.db.base_class import Base
from api.v1.catalogue.db_models import DisplayCatalogue
from api.v1.user.db_models import User
from api.v1.projects.db_models import Project
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

import uuid


class SavedAnalysis(Base):
    __tablename__ = 'saved_analysis'
    __table_args__ = {'schema': 'public'}

    saved_analysis_uuid = Column(UUID(as_uuid=True),
                                 primary_key=True,
                                 default=uuid.uuid4,
                                 unique=True,
                                 comment='Primary key id for a saved analysis')
    name = Column(String, comment='Name of the custom analysis', nullable=False)
    description = Column(String, comment='Description of the analysis')
    _geometry = Column('geometry', Geometry, comment='Geometry of the analysis', nullable=False)
    feature_type = Column(String, comment='Feature used for the analysis', nullable=False)
    zoom_level = Column(Numeric, comment='Zoom level', nullable=False)
    project_id = Column(Integer, ForeignKey(Project.project_id))
    user_id = Column(UUID(), ForeignKey(User.user_uuid),
                     comment='foreign key to the user who created this project')
    deleted_on = Column(
        DateTime, comment='Date and time when this record was deleted')
    map_layers = relationship('SavedAnalysisMapLayer', lazy='joined')

    @property
    def geometry(self):
        # geoalchemy2.Geometry outputs ewkb, let's convert it to geojson geometry
        geom = to_shape(self._geometry)
        return {
            'type': geom.geom_type,
            'coordinates': list(geom.coords)
        }

    @property
    def map_layer_list(self):
        return [x.map_layer for x in self.map_layers]


class SavedAnalysisMapLayer(Base):
    __tablename__ = 'saved_analysis_map_layer'
    __table_args__ = {'schema': 'public'}
    __table_args__ = (
        PrimaryKeyConstraint('saved_analysis_uuid', 'map_layer'),
    )

    saved_analysis_uuid = Column(UUID(as_uuid=True), ForeignKey(SavedAnalysis.saved_analysis_uuid))
    map_layer = Column(String, ForeignKey(DisplayCatalogue.display_data_name),
                       comment='Map layer id')
