SET application_name="container_setup";

create extension postgis;
create extension postgis_topology;
create extension fuzzystrmatch;
create extension postgis_tiger_geocoder;
create extension pg_stat_statements;
create extension pgaudit;
create extension plr;

alter user postgres password 'PG_ROOT_PASSWORD';

create user "PG_PRIMARY_USER" with REPLICATION  PASSWORD 'PG_PRIMARY_PASSWORD';
create user "PG_USER" with password 'PG_PASSWORD' SUPERUSER;
create user ftw_reader with password 'PG_PASSWORD';

create table primarytable (key varchar(20), value varchar(20));
grant all on primarytable to "PG_PRIMARY_USER";

create database "PG_DATABASE";

grant all privileges on database "PG_DATABASE" to "PG_USER";


\c "PG_DATABASE"

create extension postgis;
create extension postgis_topology;
create extension postgis_raster;
create extension fuzzystrmatch;
create extension postgis_tiger_geocoder;
create extension pg_stat_statements;
create extension pgaudit;
create extension plr;
create extension ltree;
create extension pg_trgm;

\c "PG_DATABASE" "PG_USER";

create schema postgis_ftw;
grant usage on schema postgis_ftw to ftw_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA postgis_ftw GRANT SELECT ON TABLES TO ftw_reader;
