"""pg_fasstr functions

Revision ID: bc8bc4bb72cb
Revises: bb906a00fbe7
Create Date: 2021-05-19 12:49:30.018297

How to populate fasstr_flows from existing HYDAT data:


  with flows as (
    select
      f.station_number,
      year,
      month,
      flow1,
      flow2,
      flow3,
      flow4,
      flow5,
      flow6,
      flow7,
      flow8,
      flow9,
      flow10,
      flow11,
      flow12,
      flow13,
      flow14,
      flow15,
      flow16,
      flow17,
      flow18,
      flow19,
      flow20,
      flow21,
      flow22,
      flow23,
      flow24,
      flow25,
      flow26,
      flow27,
      flow28,
      flow29,
      flow30,
      flow31
    from hydat.dly_flows f
    inner join hydat.stations s on s.station_number = f.station_number
    where s.prov_terr_state_loc = 'BC'
  ),
  kv as (
    select station_number, year, month, each(hstore(flows)) as kv from flows
  )
  insert into hydat.fasstr_flows (station_number, date, value)
  select
    station_number,
    to_date(concat(year::text, lpad(month::text, 2, '0'), lpad(replace((kv).key, 'flow', '')::text, 2, '0')), 'YYYYMMDD') as date,
    (kv).value::numeric as value
  from kv where (kv).key like 'flow%' and (kv).value is not null;


"""
import os
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bc8bc4bb72cb'
down_revision = 'bb906a00fbe7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'fk_fasstr_flows_station',
        'fasstr_flows', 'stations',
        ['station_number'], ['station_number'], source_schema="hydat",
        referent_schema="hydat"
    )


def downgrade():
    pass
