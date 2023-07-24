import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from api.db.base_class import BaseTable


class Base(object):
    __table_args__ = {'schema': 'metadata'}

    create_user = sa.Column(
        sa.String(100), comment='The user who created this record in the database.')
    create_date = sa.Column(
        sa.DateTime, comment='Date and time (UTC) when the physical record was created in the database.')
    update_user = sa.Column(
        sa.String(100), comment='The user who last updated this record in the database.')
    update_date = sa.Column(sa.DateTime, comment='Date and time (UTC) when the physical record was updated in the database. '
                                           'It will be the same as the create_date until the record is first '
                                           'updated after creation.')
    effective_date = sa.Column(
        sa.DateTime, comment='The date and time that the code became valid and could be used.')
    expiry_date = sa.Column(sa.DateTime, comment='The date and time after which the code is no longer valid and '
                                           'should not be used.')


Base = declarative_base(cls=Base, metadata=BaseTable.metadata)


class ModelOutputTypeCode(Base):
    __tablename__ = 'model_output_type_code'
    __table_args__ = {'schema': 'modeling'}

    model_output_type_code = sa.Column(sa.String, primary_key=True,
              comment='The output type that this regression model outputs. Possible values: MAR, 7Q2, S-7Q10, MD')
    description = sa.Column(sa.String, 
              comment='Description of the model output type.')


class MadModelCoefficients(Base):
    __tablename__ = 'mad_model_coefficients'
    __table_args__ = {'schema': 'modeling'}

    mad_model_coefficients_id = sa.Column(sa.Integer, primary_key=True)
    hydrologic_zone_id = sa.Column(sa.Integer,
              comment='TA numeric identifier assigned to a zone that represents an area of homogenous hydrologic and geomorphological characteristics.')
    model_output_type = sa.Column(sa.String, sa.ForeignKey('modeling.model_output_type_code.model_output_type_code'),
              comment='The resulting value that this multivariate model outputs. Possible values: MAR, 7Q2, S-7Q10, MD')
    month = sa.Column(sa.Integer,
              comment='The month of the year represented as an integer from 1-12 (0 if annual ouput)')
    reference_model_id = sa.Column(sa.Integer,
              comment='The model used for this zone in South Coast Stewardship Baseline (Brem, Fraser Valley South, Toba, Upper Lillooet)')
    intercept_co = sa.Column(sa.Numeric,
              comment='Intercept coefficient for the multi-variate model.')
    median_elevation_co = sa.Column(sa.Numeric,
              comment='Median elevation of the selected watershed area measured in meters (m).')
    glacial_coverage_co = sa.Column(sa.Numeric,
              comment='The amount of glacial coverage over the selected watershed area measured as a percentage (0.0-1.0).')
    precipitation_co = sa.Column(sa.Numeric,
              comment='The annual precipitation of the selected watershed area measured in milimeters per year (mm/year).')
    potential_evapo_transpiration_co = sa.Column(sa.Numeric, comment='A measure of the ability of the atmosphere to remove water through Evapo-Transpiration (ET) processes. A reference crop under optimal conditions, having the characteristics of well-watered grass with an assumed height of 12 centimeters, a fixed surface resistance of 70 seconds per meter and an albedo of 0.23.')
    drainage_area_co = sa.Column(sa.Numeric,
              comment='The drainage area of the selected watershed area measured in kilometers squared (km^2)')
    solar_exposure_co = sa.Column(sa.Numeric, comment='a surrogate variable in order to capture the effect of shadows, slope, and aspect together, a hillshade image was derived with shadows. The azimuth setting was 180° (due south) and the elevation was 45°. This roughly corresponds to noon on the 49th parallel in early summer.')
    average_slope_co = sa.Column(sa.Numeric,
              comment='The measure of rise over run (rise/run) of the selected watershed area.')
    lake_coverage_co = sa.Column(sa.Numeric,
              comment='The amount of lake coverage over the selected watershed area measured as a percentage (0.0-1.0).')
    r2 = sa.Column(sa.Float, comment='The proportion of the variance for a dependent variable thats explained by an independent variable or variables in a regression model')
    adjusted_r2 = sa.Column(sa.Float,
              comment='The correlation strength of additional variables.')
    steyx = sa.Column(sa.Float, comment='Standard error in the estimate of the hydrological variable (Y) as a function of the regression model (X).')


class WaterAllocationCoefficients(Base):
    __tablename__ = 'water_allocation_coefficients'
    __table_args__ = {'schema': 'modeling'}

    water_allocation_coefficients_id = sa.Column(sa.Integer, primary_key=True)
    economic_region_name = sa.Column(sa.String, comment='The BC economic region name that these co-efficients are used as standard values for water calculations.')
    purpose_use_code = sa.Column(sa.String, comment='The code representing the purpose use.')
    purpose_use = sa.Column(sa.String, comment='The english written purpose use.')
    rationale = sa.Column(sa.String, comment='The rationale behind where these coefficients were derived from.')
    monthly_coefficients = sa.Column(sa.ARRAY(sa.Float), nullable=False, server_default="{}", comment='Co-efficient values for each month in order from January to Decemeber.')


class WaterReturnCoefficients(Base):
    __tablename__ = 'water_return_coefficients'
    __table_args__ = {'schema': 'modeling'}
    
    water_return_coefficients_id = sa.Column(sa.Integer, primary_key=True)
    economic_region_name = sa.Column(sa.String, comment='The BC economic region name that these co-efficients are used as standard values for water calculations.')
    purpose_use_code = sa.Column(sa.String, comment='The code representing the purpose use.')
    purpose_use = sa.Column(sa.String, comment='The english written purpose use.')
    rationale = sa.Column(sa.String, comment='The rationale behind where these coefficients were derived from.')
    annual_coefficient = sa.Column(sa.Float, comment='The coefficient for annual water return for this water rights purpose.')
    monthly_coefficients = sa.Column(sa.ARRAY(sa.Float), nullable=False, server_default="{}", comment='Co-efficient values for each month in order from January to Decemeber.')