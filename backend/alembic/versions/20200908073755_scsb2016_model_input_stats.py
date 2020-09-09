"""scsb2016 model input stats

Revision ID: 3694e369419c
Revises: 369150228f9d
Create Date: 2020-09-08 07:37:55.392923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3694e369419c'
down_revision = '369150228f9d'
branch_labels = None
depends_on = None


def upgrade():
     # add allocation coefficient tables
    op.execute("create schema if not exists modeling")
    op.execute('SET search_path TO modeling')

    op.create_table(
        'scsb2016_model_input_stats',

        Column('water_model_input_stat_id', sa.Integer, primary_key=True),
        Column('input_name', sa.String, comment='Model input identifier name.'),
        Column('units', sa.String, comment='The units of the measure values.'),
        Column('minimum', sa.Float, comment='Minimum value of input found in training data.'),
        Column('maximum', sa.Float, comment='Maximum value of input found in training data.'),
        Column('median', sa.Float, comment='Median value of input found in training data.'),
        Column('average', sa.Float, comment='The average value of input found in training data.'),
        Column('standard_deviation', sa.Float, comment='The amount of variation in input values found in training data.'),


        Column('create_user', sa.String(100),
               comment='The user who created this record in the database.'),
        Column('create_date', sa.DateTime,
               comment='Date and time (UTC) when the physical record was created in the database.'),
        Column('update_user', sa.String(100),
               comment='The user who last updated this record in the database.'),
        Column('update_date', sa.DateTime,
               comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        Column('effective_date', sa.DateTime,
               comment='The date and time that the code became valid and could be used.'),
        Column('expiry_date', sa.DateTime,
               comment='The date and time after which the code is no longer valid and should not be used.')
    )

    op.execute("""
            INSERT INTO water_model_input_ranges (
                input_name,
                units,
                minimum,
                maximum,
                median,
                average,
                standard_deviation,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES
                ('drainage_area', 'km2', 4, 8430, 53, 325.01, 994.44 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('median_elevation', 'mASL', 1, 2535, 1340, 1250.83, 515.79 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('glacial_coverage', '%', 0, 0.83, 0.01, 0.102, 0.160 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('solar_exposure', '%', 0, 0.81, 0.63, 0.626, 0.053 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('potential_evapo_transpiration', 'mm/yr', 476, 825, 647, 649.64, 53.68 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('annual_precipitation', 'mm/yr', 911, 4839, 2501, 2598.66, 799.98 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('average_slope', '%*100', 0, 46, 26, 25.20, 8.29 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
                ;
        """)

    op.execute('SET search_path TO public')

def downgrade():
    pass
