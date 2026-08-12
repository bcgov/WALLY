-- =====================================================================
-- USAGE grants (all schemas, one block)
-- =====================================================================
grant usage on schema hydat, dem, hydrosheds, metadata, modeling, prism,
  tiger, tiger_data, topology, fasstr, postgis_ftw, whse_basemapping, public
  to "${appUser}";

grant usage on schema postgis_ftw to "ftw-reader";

-- =====================================================================
-- Reference/open-data schemas the app reads from at runtime (confirmed via
-- the fasstr population query, which joins against hydat). External
-- datasets loaded outside app control - grant on existing tables AND
-- default privileges so newly-added tables (e.g. dly_flows) aren't
-- silently missed.
-- =====================================================================
grant select, insert on all tables in schema hydat to "${appUser}";
grant select, insert on all tables in schema dem to "${appUser}";
grant select, insert on all tables in schema hydrosheds to "${appUser}";
grant select, insert on all tables in schema metadata to "${appUser}";
grant select, insert on all tables in schema modeling to "${appUser}";
grant select, insert on all tables in schema prism to "${appUser}";
grant select, insert on all tables in schema tiger to "${appUser}";
grant select, insert on all tables in schema tiger_data to "${appUser}";
grant select, insert on all tables in schema topology to "${appUser}";

alter default privileges in schema hydat grant select, insert on tables to "${appUser}";
alter default privileges in schema dem grant select, insert on tables to "${appUser}";
alter default privileges in schema hydrosheds grant select, insert on tables to "${appUser}";
alter default privileges in schema metadata grant select, insert on tables to "${appUser}";
alter default privileges in schema modeling grant select, insert on tables to "${appUser}";
alter default privileges in schema prism grant select, insert on tables to "${appUser}";
alter default privileges in schema tiger grant select, insert on tables to "${appUser}";
alter default privileges in schema tiger_data grant select, insert on tables to "${appUser}";
alter default privileges in schema topology grant select, insert on tables to "${appUser}";

-- =====================================================================
-- fasstr - app's own DB user access.
-- ${appUser} is a Flyway placeholder - resolved per-environment at migrate
-- time (see flyway.conf / -placeholders.appUser=... below). Pull the value
-- from the same pguser-<name> secret your app deployment already consumes
-- for POSTGRES_USER, so this can never drift out of sync with the real DB
-- user.
-- =====================================================================
grant select, insert on all tables in schema fasstr to "${appUser}";
alter default privileges in schema fasstr grant select, insert on tables to "${appUser}";

-- Functions default-grant EXECUTE to PUBLIC on creation, so the app user
-- can likely already call fasstr_calc_longterm_daily_stats /
-- fasstr_compute_frequency_quantile without this - included anyway for
-- explicitness/defense against someone later REVOKEing the PUBLIC default.
grant all on all functions in schema fasstr to "${appUser}";
alter default privileges in schema fasstr grant execute on functions to "${appUser}";

-- =====================================================================
-- postgis_ftw - app user needs its own access, not just ftw_reader.
-- =====================================================================
grant all on all tables in schema postgis_ftw to "${appUser}";
alter default privileges in schema postgis_ftw grant all on tables to "${appUser}";

alter default privileges in schema postgis_ftw grant select on tables to "ftw-reader";

-- =====================================================================
-- whse_basemapping - previously had zero grants anywhere.
-- =====================================================================
grant all on all tables in schema whse_basemapping to "${appUser}";
alter default privileges in schema whse_basemapping grant all on tables to "${appUser}";

-- =====================================================================
-- public - the app's own core business tables live here, created by
-- seed-db's prestart.sh migrations running as postgres (superuser), not
-- as ${appUser}. Without this, ${appUser} has no rights on its own app's
-- tables at runtime.
-- =====================================================================
grant create on schema public to "${appUser}";
grant select, insert, update, delete on all tables in schema public to "${appUser}";
alter default privileges in schema public grant select, insert, update, delete on tables to "${appUser}";

-- =====================================================================
-- SEQUENCE usage (all schemas, one block) - covers serial/identity columns
-- on any table ${appUser} inserts into (e.g. fasstr_flows_id_seq)
-- =====================================================================
grant usage on all sequences in schema hydat, dem, hydrosheds, metadata,
  modeling, prism, tiger, tiger_data, topology, fasstr, postgis_ftw,
  whse_basemapping, public
  to "${appUser}";

alter default privileges in schema hydat grant usage on sequences to "${appUser}";
alter default privileges in schema dem grant usage on sequences to "${appUser}";
alter default privileges in schema hydrosheds grant usage on sequences to "${appUser}";
alter default privileges in schema metadata grant usage on sequences to "${appUser}";
alter default privileges in schema modeling grant usage on sequences to "${appUser}";
alter default privileges in schema prism grant usage on sequences to "${appUser}";
alter default privileges in schema tiger grant usage on sequences to "${appUser}";
alter default privileges in schema tiger_data grant usage on sequences to "${appUser}";
alter default privileges in schema topology grant usage on sequences to "${appUser}";
alter default privileges in schema fasstr grant usage on sequences to "${appUser}";
alter default privileges in schema postgis_ftw grant usage on sequences to "${appUser}";
alter default privileges in schema whse_basemapping grant usage on sequences to "${appUser}";
alter default privileges in schema public grant usage on sequences to "${appUser}";