from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from api.db.base_class import Base


class SavedAnalysis(Base):
    __tablename__ = 'saved_analysis'
    __table_args__ = {'schema': 'public'}

    saved_analysis_id = Column(Integer, primary_key=True, comment='Primary key id for a saved '
                                                                  'analysis')
    name = Column(String, comment='Name of the custom analysis')
    description = Column(String, comment='Description of the analysis')
    geometry = Column(String, comment='Geometry of the analysis')
    feature_type = Column(String, comment='Feature used for the analysis')
    zoom_level = Column(Integer, comment='Zoom level')
    project_id = Column(Integer, ForeignKey('project.project_id'))
    user_id = Column(String, ForeignKey('user.uuid'),
                     comment='foreign key to the user who created this project')
    map_layers = relationship('SavedAnalysisMapLayer')


class SavedAnalysisMapLayer(Base):
    __tablename__ = 'saved_analysis_map_layer'
    __table_args__ = {'schema': 'public'}
    __table_args__ = (
        PrimaryKeyConstraint('saved_analysis_id', 'map_layer'),
    )

    saved_analysis_id = Column(Integer, ForeignKey('saved_analysis.saved_analysis_id'))
    map_layer = Column(String, ForeignKey('display_catalogue.display_catalogue_id'),
                       comment='Map layer id')
