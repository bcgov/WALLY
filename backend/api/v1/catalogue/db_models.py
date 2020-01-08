# coding: utf-8
from sqlalchemy import Integer, String, Column, DateTime, JSON, Text, ForeignKey, ARRAY, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, TEXT
from api.db.base_class import BaseTable

# Custom Base Class


class Base(object):
    __table_args__ = {'schema': 'metadata'}

    create_user = Column(
        String(100), comment='The user who created this record in the database.')
    create_date = Column(
        DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = Column(
        String(100), comment='The user who last updated this record in the database.')
    update_date = Column(DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = Column(
        DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = Column(DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


Base = declarative_base(cls=Base, metadata=BaseTable.metadata)


# Data Storage Tables
class DataStore(Base):
    __tablename__ = 'data_store'

    data_store_id = Column(Integer, primary_key=True)

    name = Column(String, comment='data store detail name', index=True)
    description = Column(
        String, comment='explanation behind data store and use case')
    time_relevance = Column(
        Integer, comment='how long before this data store becomes stale, measured in DAYS')
    last_updated = Column(
        DateTime, comment='last time data store was updated from sources')

    data_sources = relationship("DataSource")


class DataFormatCode(Base):
    __tablename__ = 'data_format_code'
    data_format_code = Column(String, primary_key=True, comment='source data format, options: '
                                                                'wms, csv, excel, sqlite, text, json')
    description = Column(String, comment='code type description')


class DataSource(Base):
    __tablename__ = 'data_source'

    data_source_id = Column(Integer, primary_key=True)

    name = Column(String, comment='data source detail name', index=True)
    description = Column(
        String, comment='explanation behind data source and use case')
    source_url = Column(String, comment='root source url of data')

    data_format_code = Column(String, ForeignKey('metadata.data_format_code.data_format_code'),
                              comment='format type of the source information')
    data_format = relationship('DataFormatCode')

    data_store_id = Column(Integer, ForeignKey('metadata.data_store.data_store_id'),
                           comment='related data store where this sources data is held after ETL')
    data_store = relationship("DataStore")

    source_object_name = Column(String, nullable=True,
                                comment='The object name reference at the external data source.  This is used to lookup datasets on directories like DataBC, e.g. WHSE_WATER_MANAGEMENT.GW_AQUIFERS_CLASSIFICATION_SVW')
    data_table_name = Column(String, nullable=False,
                             comment='The table name where data for a map layer is stored. Used to help ogr2ogr and pgloader reference the correct table when processing new map layer data.')
    last_updated_data = Column(DateTime, server_default=text('2019-01-01'), nullable=False,
                               comment='The date the data for this map layer was last updated in the database.')
    last_updated_tiles = Column(DateTime, server_default=text('2019-01-01'), nullable=False,
                                comment='The date the tiles for this map layer were last re-generated and made available on the tile server. Should be as close as possible to last_updated_data, but differences are expected due to tile processing times.')
    direct_link = Column(
        String, nullable=True, comment='A direct link to download the dataset from the source, if available.')
    source_object_id = Column(String, nullable=True,
                              comment='The ID on the upstream data source. This is specifically required for paging through the DataBC API. Note: do not rely on these IDs as permanent keys, only for sorting and paginating during queries (e.g. `sortBy=WLS_WRL_SYSID&startIndex=1000`)')


class ApiCatalogue(Base):
    __tablename__ = 'api_catalogue'
    api_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='api endpoint description')
    url = Column(
        String, comment='an internal api endpoint that serves all data points for a display layer')


class WmsCatalogue(Base):
    __tablename__ = 'wms_catalogue'
    wms_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='wms layer description')
    wms_name = Column(
        String, comment='identifying layer name with the data bc wms server')
    wms_style = Column(
        String,
        comment='style key to display data in different visualizations for wms layer',
        nullable=False, default='')


class VectorCatalogue(Base):
    __tablename__ = 'vector_catalogue'
    vector_catalogue_id = Column(Integer, primary_key=True)
    description = Column(String, comment='vector layer description')
    vector_name = Column(String, comment='identifying vector layer name')


class DisplayCatalogue(Base):
    __tablename__ = 'display_catalogue'
    display_catalogue_id = Column(Integer, primary_key=True)

    display_name = Column(
        String, comment='this is the public name of the display layer')
    display_data_name = Column(String(200), unique=True,
                               comment='this is the main business key used throughout the application to '
                               'identify data layers and connect data to templates.')
    label = Column(String, comment='label for label_column value')
    label_column = Column(
        String, comment='we use this column value as a list item label in the client')
    highlight_columns = Column(ARRAY(TEXT), comment='the key columns that have business value to the end user. '
                               'We primarily will only show these columns in the '
                               'client and report')

    api_catalogue_id = Column(Integer, ForeignKey('metadata.api_catalogue.api_catalogue_id'),
                              comment='references api catalogue item')
    api_catalogue = relationship("ApiCatalogue")

    wms_catalogue_id = Column(Integer, ForeignKey('metadata.wms_catalogue.wms_catalogue_id'),
                              comment='references wms catalogue item')
    wms_catalogue = relationship("WmsCatalogue")

    vector_catalogue_id = Column(Integer, ForeignKey('metadata.vector_catalogue.vector_catalogue_id'),
                                 comment='references vector catalogue item')
    vector_catalogue = relationship("VectorCatalogue")

    display_templates = relationship(
        "DisplayTemplateDisplayCatalogueXref", back_populates="display_catalogue")

    layer_category_code = Column(String, ForeignKey(
        'metadata.layer_category.layer_category_code'), comment='references a layer category')
    layer_category = relationship("LayerCategory", back_populates="layers")

    data_source_id = Column(Integer, ForeignKey('metadata.data_source.data_source_id'),
                            comment='references catalogue data source')
    data_source = relationship("DataSource")
    required_map_properties = Column(ARRAY(TEXT), nullable=False, server_default='{}',
                                     comment='Properties that are required by the map for rendering markers/shapes, e.g. for colouring markers based on a value or property like POD_SUBTYPE')
    mapbox_source_id = Column(String, ForeignKey('metadata.mapbox_source.mapbox_source_id'), nullable=True)


class DisplayTemplate(Base):
    __tablename__ = 'display_template'
    display_template_id = Column(Integer, primary_key=True)

    title = Column(
        String, comment='title to be used for headers and labels for template')
    display_order = Column(
        Integer, comment='determines which components are shown first to last in 100s')

    display_data_names = Column(ARRAY(TEXT), comment='unique business keys that represent the required layers '
                                                     'used to hydrate this display template')

    override_key = Column(String, unique=True, comment='unique business key that is used to override '
                                                       'default builder method during template hydration. '
                                                       'optional field, if null then use default builder')

    display_catalogues = relationship(
        "DisplayTemplateDisplayCatalogueXref", back_populates="display_template")

    link_components = relationship("LinkComponent")
    chart_components = relationship("ChartComponent")
    image_components = relationship("ImageComponent")
    formula_components = relationship("FormulaComponent")


class DisplayTemplateDisplayCatalogueXref(Base):
    __tablename__ = 'display_template_display_catalogue_xref'
    # display_template_display_catalogue_xref_id = Column(Integer, primary_key=True)
    display_template_id = Column(Integer, ForeignKey(
        'metadata.display_template.display_template_id'), primary_key=True)
    display_catalogue_id = Column(Integer, ForeignKey(
        'metadata.display_catalogue.display_catalogue_id'), primary_key=True)

    display_catalogue = relationship(
        "DisplayCatalogue", back_populates="display_templates")
    display_template = relationship(
        "DisplayTemplate", back_populates="display_catalogues")


class ComponentTypeCode(Base):
    __tablename__ = 'component_type_code'
    component_type_code = Column(String, primary_key=True,
                                 comment='components have many different types, which determines what business '
                                         'logic to use when constructing the component.')
    description = Column(
        String, comment='explanation of component type and use case')


class ChartComponent(Base):
    __tablename__ = 'chart_component'
    chart_component_id = Column(Integer, primary_key=True)
    chart_title = Column(
        String, comment='title to be used for headers and labels for components')
    component_type_code = Column(String, ForeignKey('metadata.component_type_code.component_type_code'),
                                 comment='component type used for rendering functionality')
    component_type = relationship('ComponentTypeCode')
    display_order = Column(
        Integer, comment='determines which components are shown first to last in 100s')
    chart = Column(
        JSON, comment='this holds the chart js json schema to use in the client and reporting')
    labels_key = Column(
        String, comment='the key used to generate the labels array')
    dataset_keys = Column(
        ARRAY(TEXT), comment='the keys used to generate the raw data for chart datasets')
    display_template_id = Column(Integer, ForeignKey('metadata.display_template.display_template_id'),
                                 comment='reference to parent display template')


class LinkComponent(Base):
    __tablename__ = 'link_component'
    link_component_id = Column(Integer, primary_key=True)
    link_title = Column(
        String, comment='title to be used for headers and labels for components')
    component_type_code = Column(String, ForeignKey('metadata.component_type_code.component_type_code'),
                                 comment='component type used for rendering functionality')
    component_type = relationship('ComponentTypeCode')
    display_order = Column(
        Integer, comment='determines which components are shown first to last in 100s')
    link_pattern = Column(
        String, comment='url pattern to source document or web page')
    link_pattern_keys = Column(
        ARRAY(String), comment='keys to plug into link pattern')
    link_label_key = Column(
        String, comment='key which creates the clickable text for the link')
    display_template_id = Column(Integer, ForeignKey('metadata.display_template.display_template_id'),
                                 comment='reference to parent display template')


class ImageComponent(Base):
    __tablename__ = 'image_component'
    image_component_id = Column(Integer, primary_key=True)
    image_title = Column(
        String, comment='title to be used for headers and labels for components')
    component_type_code = Column(String, ForeignKey('metadata.component_type_code.component_type_code'),
                                 comment='component type used for rendering functionality')
    component_type = relationship('ComponentTypeCode')
    display_order = Column(
        Integer, comment='determines which components are shown first to last in 100s')
    width = Column(Integer, comment='x size of image')
    height = Column(Integer, comment='y size of image')
    url = Column(String, comment='source url to image source')
    display_template_id = Column(Integer, ForeignKey('metadata.display_template.display_template_id'),
                                 comment='reference to parent display template')


class FormulaComponent(Base):
    __tablename__ = 'formula_component'
    formula_component_id = Column(Integer, primary_key=True)
    formula_title = Column(
        String, comment='title to be used for headers and labels for components')
    component_type_code = Column(String, ForeignKey('metadata.component_type_code.component_type_code'),
                                 comment='component type used for rendering functionality')
    component_type = relationship('ComponentTypeCode')
    display_order = Column(
        Integer, comment='determines which components are shown first to last in 100s')
    formula_component = Column(JSON, comment='formula layout for calculation')
    display_template_id = Column(Integer, ForeignKey('metadata.display_template.display_template_id'),
                                 comment='reference to parent display template')


class LayerCategory(Base):
    __tablename__ = 'layer_category'
    layer_category_code = Column(String, primary_key=True)
    description = Column(String(length=255))
    layers = relationship("DisplayCatalogue", back_populates="layer_category")
    display_order = Column(Integer)


class MapboxSource(Base):
    __tablename__ = 'mapbox_source'
    mapbox_source_id = Column(String, primary_key=True)
    max_zoom = Column(Integer)
