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
create table if not exists fasstr.fasstr_flows (
  id serial primary key,
  station_number text,
  date date,
  value numeric
);

create index if not exists idx_fasstr_flows_station on fasstr.fasstr_flows(station_number);


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
