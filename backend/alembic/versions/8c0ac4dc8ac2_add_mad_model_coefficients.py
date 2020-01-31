"""add mad model coefficients

Revision ID: 8c0ac4dc8ac2
Revises: 9ee500c7ad08
Create Date: 2020-01-30 20:28:09.565290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey


# revision identifiers, used by Alembic.
revision = '8c0ac4dc8ac2'
down_revision = '9ee500c7ad08'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema if not exists modeling")
    op.execute('SET search_path TO modeling')

    op.create_table(
      'model_output_type_code',
      sa.Column('model_output_type_code', sa.String, primary_key=True,
                  comment='The output type that this regression model outputs. Possible values: MAR, 7Q2, S-7Q10, MD')
    )

    op.create_table(
        'mad_model_coefficients',
        Column('mad_model_coefficients_id', sa.Integer, primary_key=True),
        Column('hydrologic_zone_id', sa.Integer, comment='TA numeric identifier assigned to a zone that represents an area of homogenous hydrologic and geomorphological characteristics.'),
        Column('model_output_type', sa.String, ForeignKey('modeling.model_output_type_code.model_output_type_code'),
                comment='The resulting value that this multivariate model outputs. Possible values: MAR, 7Q2, S-7Q10, MD'),
        Column('month', sa.Integer, comment='The month of the year represented as an integer from 1-12 (0 if annual ouput)'),
        Column('reference_model_id', sa.Integer, comment='The model used for this zone in South Coast Stewardship Baseline (Brem, Fraser Valley South, Toba, Upper Lillooet)'),
        Column('intercept_co', sa.Float, comment='Intercept coefficient for the multi-variate model.'),
        Column('median_elevation_co', sa.Float, comment='Median elevation of the selected watershed area measured in meters (m).'),
        Column('glacial_coverage_co', sa.Float, comment='The amount of glacial coverage over the selected watershed area measured as a percentage (0.0-1.0).'),
        Column('precipitation_co', sa.Float, comment='The annual precipitation of the selected watershed area measured in milimeters per year (mm/year).'),
        Column('potential_evapo_transpiration_co', sa.Float, comment='A measure of the ability of the atmosphere to remove water through Evapo-Transpiration (ET) processes. A reference crop under optimal conditions, having the characteristics of well-watered grass with an assumed height of 12 centimeters, a fixed surface resistance of 70 seconds per meter and an albedo of 0.23.'),
        Column('drainage_area_co', sa.Float, comment='The drainage area of the selected watershed area measured in kilometers squared (km^2)'),
        Column('solar_exposure_co', sa.Float, comment='a surrogate variable in order to capture the effect of shadows, slope, and aspect together, a hillshade image was derived with shadows. The azimuth setting was 180° (due south) and the elevation was 45°. This roughly corresponds to noon on the 49th parallel in early summer.'),
        Column('average_slope_co', sa.Float, comment='The measure of rise over run (rise/run) of the selected watershed area.'),
        Column('r2', sa.Float, comment='The proportion of the variance for a dependent variable thats explained by an independent variable or variables in a regression model'),
        Column('adjusted_r2', sa.Float, comment='The correlation strength of additional variables.'),
        Column('steyx', sa.Float, comment='Standard error in the estimate of the hydrological variable (Y) as a function of the regression model (X).'),
        Column('lake_coverage_co', sa.Float, comment='The amount of lake coverage over the selected watershed area measured as a percentage (0.0-1.0).'),

        Column('create_user', sa.String(100), comment='The user who created this record in the database.'),
        Column('create_date', sa.DateTime, comment='Date and time (UTC) when the physical record was created in the database.'),
        Column('update_user', sa.String(100), comment='The user who last updated this record in the database.'),
        Column('update_date', sa.DateTime, comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        Column('effective_date', sa.DateTime, comment='The date and time that the code became valid and could be used.'),
        Column('expiry_date', sa.DateTime, comment='The date and time after which the code is no longer valid and should not be used.')
    )
    
    op.execute("""
        INSERT INTO model_output_type_code (
            model_output_type_code,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) VALUES 
            ('MAR', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            ('7Q2', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            ('S-7Q10', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            ('MD', 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
        ;
    """)

    op.execute("""
        INSERT INTO mad_model_coefficients (
            hydrologic_zone_id,
            model_output_type,
            month,
            reference_model_id,
            intercept_co,
            median_elevation_co,
            glacial_coverage_co,
            precipitation_co,
            potential_evapo_transpiration_co,
            drainage_area_co,
            solar_exposure_co,
            average_slope_co,
            r2,
            adjusted_r2,
            steyx,
            create_user, create_date, update_user, update_date, effective_date, expiry_date
        ) VALUES 
            (25, 'MAR', 0, 12, -30.05, 0, 0, 0.0162, 0, 0.00369, 0, 1.39, 0.97, 0.96, 4.16, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, '7Q2', 0, 12, 0.81, 0, -0.057, 0, -0.00102, -0.000006, 0, 0, 0.63, 0.52, 0.032, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'S-7Q10', 0, 12, 1.90, 0.000314, 0.685, 0, -0.0032, 0, 0, 0, 0.88, 0.83, 0.04, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 1, 13, 0.04, 0, -0.0512, 0.00000453, -0.0000216, 0, 0, 0, 0.62, 0.49, 0.001, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 2, 13, 0.00, 0, -0.0388, 0.00000342, 0.0000338, 0, 0, 0, 0.68, 0.58, 0.003, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 3, 13, -0.05, 0, -0.0475, 0.0000049, 0.00012, 0, 0, 0, 0.86, 0.81, 0.004, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 4, 13, -0.30, 0, -0.146, 0.00000433, 0.000578, 0, 0, 0, 0.94, 0.92, 0.012, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 5, 13, -0.58, 0, -0.60, -0.0000127, 0.00129, 0, 0, 0, 0.95, 0.93, 0.025, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 6, 13, 0.12, 0, -0.434, -0.00000682, 0.000205, 0, 0, 0, 0.84, 0.78, 0.023, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 7, 13, 0.66, 0, 0.381, 0.00000808, -0.000842, 0, 0, 0, 0.86, 0.81, 0.036, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 8, 13, 0.57, 0, 0.670, -0.00000763, -0.000778, 0, 0, 0, 0.96, 0.94, 0.021, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 9, 13, 0.33, 0, 0.369, -0.00000622, -0.000446, 0, 0, 0, 0.96, 0.95, 0.012, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 10, 13, 0.22, 0, 0.0931, -0.000000490, -0.000273, 0, 0, 0, 0.83, 0.77, 0.01, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 11, 13, 0.07, 0, -0.0676, 0.0000129, -0.0000620, 0, 0, 0, 0.66, 0.55, 0.008, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (25, 'MD', 12, 13, 0.04, 0, -0.0708, 0.00000628, -0.0000275, 0, 0, 0, 0.61, 0.48, 0.005, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            
            (26, 'MAR', 0, 13, -83.53, 0, 124, 0.0246, 0.121, 0, 0, 0, 0.70, 0.65, 13.8, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, '7Q2', 0, 12, 0.53, 0, -0.692, 0, -0.000478, 0.0000198, 0, 0, 0.61, 0.54, 0.043, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'S-7Q10', 0, 12, 1.15, 0, 0.717, 0, -0.00143, 0.0000314, 0, 0, 0.86, 0.83, 0.053, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 1, 12, 0.02, 0.0000141, -0.219, 0.00000788, 0, 0, 0, 0, 0.88, 0.85, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 2, 13, 0.02, -0.0000181, -0.125, 0, 0.0000875, 0, 0, 0, 0.78, 0.72, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 3, 13, -0.02, -0.0000237, -0.101, 0, 0.000161, 0, 0, 0, 0.83, 0.79, 0.008, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 4, 13, -0.06, -0.0000375, -0.0359, 0, 0.000276, 0, 0, 0, 0.76, 0.70, 0.011, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 5, 13, -0.10, -0.0000212, -0.0199, 0, 0.000420, 0, 0, 0, 0.51, 0.38, 0.021, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 6, 12, 0.14, 0.0000440, 0.00498, -0.0000122, 0, 0, 0, 0, 0.71, 0.63, 0.011, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 7, 12, 0.05, 0.0000697, 0.306, -0.00000988, 0, 0, 0, 0, 0.85, 0.81, 0.014, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 8, 13, 0.11, 0.0000916, 0.342, 0, -0.000255, 0, 0, 0, 0.91, 0.88, 0.016, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 9, 13, 0.24, 0.000000849, 0.184, 0, -0.000307, 0, 0, 0, 0.85, 0.81, 0.012, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 10, 13, 0.33, -0.0000778, 0.105, 0, -0.000261, 0, 0, 0, 0.83, 0.78, 0.006, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 11, 12, 0.08, -0.00000985, -0.169, 0.00000881, 0, 0, 0, 0, 0.87, 0.83, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (26, 'MD', 12, 12, 0.07, -0.00000255, -0.249, 0.00000412, 0, 0, 0, 0, 0.86, 0.82, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            
            (27, 'MAR', 0, 12, -13.24, -0.00421, 0, 0.0248, 0, 0, 0, 1.36, 0.90, 0.89, 13, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, '7Q2', 0, 12, 0.49, 0, 0, 0, -0.0000649, 0, -0.556, 0.00228, 0.52, 0.44, 0.04, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'S-7Q10', 0, 12, 0.40, 0, 0, 0, -0.0000303, 0, -0.484, 0.00191, 0.48, 0.39, 0.037, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 1, 12, 0.18, -0.0000690, 0, -0.00000613, 0, -0.0000251, 0, 0, 0.94, 0.92, 0.025, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 2, 13, 0.13, 0, 0, -0.0000244, 0, -0.0000305, 0.0589, 0, 0.93, 0.91, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 3, 12, 0.15, 0.0000125, 0, -0.0000205, 0, -0.0000359, 0, 0, 0.83, 0.78, 0.005, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 4, 12, 0.10, 0.0000507, 0, -0.0000138, 0, -0.00000758, 0, 0, 0.54, 0.42, 0.004, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 5, 12, 0.02, 0.0000457, 0, 0.0000135, 0, 0.0000770, 0, 0, 0.86, 0.83, 0.01, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 6, 13, 0.15, 0, 0, 0.0000320, 0, 0.0000847, -0.253, 0, 0.90, 0.87, 0.006, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 7, 12, -0.04, -0.0000403, 0, 0.0000335, 0, 0.0000992, 0, 0, 0.90, 0.88, 0.007, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 8, 12, -0.01, -0.0000230, 0, 0.0000153, 0, 0.0000435, 0, 0, 0.81, 0.75, 0.003, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 9, 12, 0.01, 0.00000639, 0, 0.00000368, 0, 0.0000123, 0, 0, 0.61, 0.50, 0.005, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 10, 13, -0.06, 0, 0, 0.0000178, 0, 0.0000332, 0.100, 0, 0.88, 0.85, 0.004, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 11, 13, 0.05, 0, 0, -0.00000842, 0, -0.0000575, 0.157, 0, 0.42, 0.26, 0.011, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
            (27, 'MD', 12, 13, 0.14, 0, 0, -0.0000321, 0, -0.0000955, 0.120, 0, 0.94, 0.92, 0.010, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
        ;
    """)

    op.execute('SET search_path TO public')


def downgrade():
    pass
