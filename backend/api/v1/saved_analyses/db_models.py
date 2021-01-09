from sqlalchemy import String, Column, DateTime, ARRAY, TEXT, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from api.v1.catalogue.db_models import DisplayCatalogue

from api.db.base_class import Base


class SavedAnalysis(Base):
    __tablename__ = 'saved_analysis'
    __table_args__ = {'schema': 'public'}

    saved_analysis_id = Column(Integer, primary_key=True, comment='Primary key id for a saved '
                                                                  'analysis')
    description = Column(String, comment='Description of the analysis')
    name = Column(String, comment='Name of the custom analyses')
    geometry = Column(String)
    feature_type = Column(String)
    zoom_level = Column(Integer, comment='Zoom level')
    user_id = Column(String, ForeignKey('user.uuid'),
                     comment='foreign key to the user who created this project')

    project_id = Column(Integer, ForeignKey('project.project_id'),
                        comment='foreign key to the project this analysis is associated with')
    map_layers = relationship("SavedAnalysisMapLayer", back_populates="save_analysis")


class SavedAnalysisMapLayer(Base):
    __tablename__ = 'saved_analysis_map_layer'
    __table_args__ = {'schema': 'public'}

    saved_analysis_id = Column(Integer, ForeignKey(SavedAnalysis.saved_analysis_id),
                               primary_key=True)
    map_layer_name = Column(String, ForeignKey(DisplayCatalogue.display_data_name),
                            primary_key=True)
    map_layer = relationship(DisplayCatalogue)
    save_analysis = relationship(SavedAnalysis, back_populates="map_layers")
