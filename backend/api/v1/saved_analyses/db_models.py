from sqlalchemy import String, Column, DateTime, ARRAY, TEXT, Integer, ForeignKey
from api.db.base_class import Base


class SavedAnalysis(Base):
    __tablename__ = 'saved_analysis'
    __table_args__ = {'schema': 'public'}

    saved_analysis_id = Column(Integer, primary_key=True, comment='Primary key id for a saved '
                                                                  'analysis')
    description = Column(String, comment='Description of the analysis')
    name = Column(String, comment='Name of the custom analyses')
    shape = Column(String)
    feature_type = Column(String)
    zoom_level = Column(Integer, comment='Zoom level')


class ProjectSavedAnalysis(Base):
    __tablename__ = 'project_saved_analysis'
    __table_args__ = {'schema': 'public'}

    project_id = Column(Integer, ForeignKey('project.project_id'),
                    comment='foreign key to the project this document is associated with')

    saved_analysis_id = Column(Integer, ForeignKey('saved_analysis.saved_analysis_id'),
                    comment='foreign key to the project this document is associated with')


class SavedAnalysisMapLayer(Base):
    __tablename__ = 'saved_analysis_map_layer'
    __table_args__ = {'schema': 'public'}

    saved_analysis_id = Column(Integer, ForeignKey('saved_analysis.saved_analysis_id'))
    map_layer = Column(String, ForeignKey('metadata.display_catalogue.display_data_name'),
                       comment='Layer Display Data Name')
