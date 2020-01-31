"""add mad model coefficients

Revision ID: 8c0ac4dc8ac2
Revises: 9ee500c7ad08
Create Date: 2020-01-30 20:28:09.565290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c0ac4dc8ac2'
down_revision = '9ee500c7ad08'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema if not exists modeling")
    op.execute('SET search_path TO modeling')

    op.create_table(
        'mad_model_coefficients',
        Column('mad_model_coefficients_id', sa.Integer, primary_key=True),
        Column('model_output_type', sa.Integer, comment='The resulting value that this multivariate model outputs. Possible values: MAR, 7Q2, S-7Q10, MD'),
        Column('reference_model_id', sa.Integer, comment='The model used for this zone in South Coast Stewardship Baseline (Brem, Fraser Valley South, Toba, Upper Lillooet)'),
        Column('hydrologic_zone_id', sa.Integer, comment='TA numeric identifier assigned to a zone that represents an area of homogenous hydrologic and geomorphological characteristics.'),
        Column('month', sa.Integer, comment='The month of the year represented as an integer from 1-12'),
        Column('intercept_co', sa.Float, comment='Intercept coefficient for the multi-variate model.'),
        Column('median_elevation_co', sa.Float, comment='Median elevation of the selected watershed area measured in meters (m).'),
        Column('lake_coverage_co', sa.Float, comment='The amount of lake coverage over the selected watershed area measure as a percentage (0.0-1.0).'),
        Column('glacial_coverage_co', sa.Float, comment='The amount of glacial coverage over the selected watershed area measured as a percentage (0.0-1.0).'),
        Column('annual_precipitation_co', sa.Float, comment='The annual precipitation of the selected watershed area measured in milimeters per year (mm/year).'),
        Column('potential_evapo_transpiration_co', sa.Float, comment='A measure of the ability of the atmosphere to remove water through Evapo-Transpiration (ET) processes. A reference crop under optimal conditions, having the characteristics of well-watered grass with an assumed height of 12 centimeters, a fixed surface resistance of 70 seconds per meter and an albedo of 0.23.'),
        Column('drainage_area_co', sa.Float, comment='The drainage area of the selected watershed area measured in kilometers squared (km^2)'),
        Column('solar_exposure_co', sa.Float, comment='a surrogate variable in order to capture the effect of shadows, slope, and aspect together, a hillshade image was derived with shadows. The azimuth setting was 180° (due south) and the elevation was 45°. This roughly corresponds to noon on the 49th parallel in early summer.'),
        Column('average_slope_co', sa.Float, comment='The measure of rise over run (rise/run) of the selected watershed area.'),
        Column('r2', sa.Float, comment='The proportion of the variance for a dependent variable thats explained by an independent variable or variables in a regression model'),
        Column('adjusted_r2', sa.Float, comment='The correlation strength of additional variables.'),
        Column('steyx', sa.Float, comment='Standard error in the estimate of the hydrological variable (Y) as a function of the regression model (X).'),

        Column('create_user', sa.String(100), comment='The user who created this record in the database.'),
        Column('create_date', sa.DateTime, comment='Date and time (UTC) when the physical record was created in the database.'),
        Column('update_user', sa.String(100), comment='The user who last updated this record in the database.'),
        Column('update_date', sa.DateTime, comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        Column('effective_date', sa.DateTime, comment='The date and time that the code became valid and could be used.'),
        Column('expiry_date', sa.DateTime, comment='The date and time after which the code is no longer valid and should not be used.')
    )

    op.create_table(
      'model_output_type',
      Column('type', sa.String, primary_key=True),
    )

    op.execute("""
        INSERT INTO mad_model_coefficients (
            model_output_type,
            reference_model_id,
            hydrologic_zone_id,
            month,
            intercept_co,
            median_elevation_co,
            lake_coverage_co,
            glacial_coverage_co,
            annual_precipitation_co,
            potential_evapo_transpiration_co,
            drainage_area_co,
            solar_exposure_co,
            average_slope_co,
            r2,
            adjusted_r2,
            steyx,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) VALUES 
            ('02I28', 'Indl Waste Mgmt: Sewage Disposal', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            ('02I04', 'Conveying (Inactive)', ARRAY[ 1,1,1,1,1,1,1,1,1,1,1,1 ], 'from Ecofish Baseline Report and Rood and Hamilton (1995)', 'Lower Mainland--Southwest', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
        ;
    """)

    op.execute('SET search_path TO public')


def downgrade():
    pass
