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

        sa.Column('water_model_input_stat_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, comment='Model input identifier name.'),
        sa.Column('units', sa.String,
                  comment='The units of the measure values.'),
        sa.Column('minimum', sa.Float,
                  comment='Minimum value of input found in training data.'),
        sa.Column('maximum', sa.Float,
                  comment='Maximum value of input found in training data.'),
        sa.Column('median', sa.Float,
                  comment='Median value of input found in training data.'),
        sa.Column('average', sa.Float,
                  comment='The average value of input found in training data.'),
        sa.Column('standard_deviation', sa.Float,
                  comment='The amount of variation in input values found in training data.'),
        sa.Column('quartile_1', sa.Float,
                  comment='The first quarter marker value in the training data.'),
        sa.Column('quartile_3', sa.Float,
                  comment='The third quarter marker value in the training data.'),

        sa.Column('create_user', sa.String(100),
                  comment='The user who created this record in the database.'),
        sa.Column('create_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was created in the database.'),
        sa.Column('update_user', sa.String(100),
                  comment='The user who last updated this record in the database.'),
        sa.Column('update_date', sa.DateTime,
                  comment='Date and time (UTC) when the physical record was updated in the database. It will be the same as the create_date until the record is first updated after creation.'),
        sa.Column('effective_date', sa.DateTime,
                  comment='The date and time that the code became valid and could be used.'),
        sa.Column('expiry_date', sa.DateTime,
                  comment='The date and time after which the code is no longer valid and should not be used.')
    )

    op.execute("""
            INSERT INTO scsb2016_model_input_stats (
                name,
                units,
                minimum,
                maximum,
                median,
                average,
                standard_deviation,
                quartile_1,
                quartile_3,
                create_user, create_date, update_user, update_date, effective_date, expiry_date
            ) VALUES
                ('drainage_area', 'km2', 4, 8430, 53, 325.01, 994.44, 28, 152, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('median_elevation', 'mASL', 1, 2535, 1340, 1250.83, 515.79, 1008, 1616.5, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('glacial_coverage', '%', 0, 0.83, 0.01, 0.102, 0.160, 0, 0.17, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('solar_exposure', '%', 0, 0.81, 0.63, 0.626, 0.053, 0.6, 0.66, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('potential_evapo_transpiration', 'mm/yr', 476, 825, 647, 649.64, 53.68, 614.5, 675.5, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('annual_precipitation', 'mm/yr', 911, 4839, 2501, 2598.66, 799.98, 2036.5, 3235.5, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z'),
                ('average_slope', '%*100', 0, 46, 26, 25.20, 8.29, 22, 30, 'ETL_USER', CURRENT_DATE, 'ETL_USER', CURRENT_DATE, CURRENT_DATE, '9999-12-31T23:59:59Z')
                ;
        """)

    op.execute('SET search_path TO public')


def downgrade():
    pass
