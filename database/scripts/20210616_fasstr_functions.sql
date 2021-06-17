-- set up FASSTR functions
-- These functions use the PL/R extension to call functions in the FASSTR R library.
-- see https://github.com/bcgov/fasstr

-- add FASSTR to the plr_modules table, which will pre-load libraries
-- on db startup.
create table if not exists public.plr_modules (modseq int4, modsrc text);

insert into public.plr_modules 
select (select max(modseq) + 1 from plr_modules), 'library("fasstr")'
where not exists (
  select * from plr_modules where modsrc = 'library("fasstr")'
);

create schema if not exists fasstr;

-- create a table with date - value columns to store HYDAT flow data
-- in a format more similar to a time series set.
create table fasstr.fasstr_flows (
  id serial primary key,
  station_number text,
  date date,
  value numeric
);

create index idx_fasstr_flows_station on fasstr.fasstr_flows(station_number);


-- longterm_stats is a helper table that defines the members and types
-- that are returned by fasstr_longterm_daily_stats.  This is required
-- by PL/R to convert from R types to Postgres types.
create table if not exists fasstr.longterm_stats (
  month text,
  mean numeric,
  median numeric,
  maximum numeric,
  minimum numeric,
  p10 numeric,
  p90 numeric
);


-- fasstr_calc_longterm_daily_stats
-- example: select * from fasstr_calc_longterm_daily_stats('08NM116')

-- accepts two arrays for dates and args
create or replace function fasstr.fasstr_calc_longterm_daily_stats(
  dates date[],
  flows numeric[],
  ignore_missing boolean default FALSE,
  complete_years boolean default FALSE
)
returns setof fasstr.longterm_stats as
$$
  library(fasstr)

  flowdata <- data.frame(Date = dates, Value = flows)
  x <- fasstr::calc_longterm_daily_stats(
    data=flowdata,
    ignore_missing=ignore_missing,
    complete_years=complete_years
  )

  names(x) <- tolower(names(x))
  return(x)
$$
LANGUAGE 'plr' VOLATILE STRICT;

-- accepts a `station_number` value from the fasstr_flows table.
create or replace function fasstr.fasstr_calc_longterm_daily_stats(
  stn text,
  ignore_missing boolean default FALSE,
  complete_years boolean default FALSE
)
returns setof fasstr.longterm_stats as
$$
  with flowdata as (
    select array_agg(value) as values, array_agg(date) as dates from fasstr.fasstr_flows where station_number = stn
  )
  select fasstr.fasstr_calc_longterm_daily_stats(dates, values, ignore_missing, complete_years) from flowdata
$$
LANGUAGE 'sql'
;

-- fasstr_compute_frequency_quantile
-- 
-- examples:
-- 30 day average, 10 year return (30Q10-A)
-- select fasstr_compute_frequency_quantile('08NM116', roll_days => 30, return_period => 10 );
--
-- 7 day average, 10 year return (7Q10-A)
-- select fasstr_compute_frequency_quantile('08NM116', roll_days => 7, return_period => 10 );
--
-- 30 day average, 10 year return, Summer (30Q10-S)
-- select fasstr_compute_frequency_quantile('08NM116', roll_days => 7, return_period => 10, summer=> true );

create or replace function fasstr.fasstr_compute_frequency_quantile(
  dates date[],
  flows numeric[],
  roll_days integer,
  return_period integer,
  summer boolean default FALSE,
  ignore_missing boolean default FALSE
)
returns numeric as
$$
  library(fasstr)

  months <- if (summer == TRUE) 7:9 else 1:12

  flowdata <- data.frame(Date = dates, Value = flows)
  x <- fasstr::compute_frequency_quantile(
    data=flowdata,
    roll_days=roll_days,
    return_period=return_period,
    months=months,
    ignore_missing=ignore_missing
  )

  return(x)
$$
LANGUAGE 'plr' VOLATILE STRICT;

-- accepts a `station_number` value from the fasstr_flows table.
-- this function creates arrays from the `fasstr_flows` table
-- and then calls the fasstr_compute_frequency_quantile(date[], numeric[], ...)
create or replace function fasstr.fasstr_compute_frequency_quantile(
  stn text,
  roll_days integer,
  return_period integer,
  summer boolean default FALSE,
  ignore_missing boolean default FALSE
)
returns numeric as
$$
  with flowdata as (
    select array_agg(value) as values, array_agg(date) as dates from fasstr.fasstr_flows where station_number = stn
  )
  select fasstr.fasstr_compute_frequency_quantile(dates, values, roll_days, return_period, summer, ignore_missing) from flowdata
$$
LANGUAGE 'sql'
;
