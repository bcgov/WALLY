-- Grants for the app's own DB user against fasstr and postgis_ftw.
-- ${appUser} is a Flyway placeholder - resolved per-environment at migrate time
-- (see flyway.conf / -placeholders.appUser=... below). Pull the value from
-- the same pguser-<name> secret your app deployment already consumes for
-- POSTGRES_USER, so this can never drift out of sync with the real DB user.

grant usage on schema fasstr to "${appUser}";
grant select on all tables in schema fasstr to "${appUser}";
alter default privileges in schema fasstr grant select on tables to "${appUser}";

-- Functions default-grant EXECUTE to PUBLIC on creation, so the app user can
-- likely already call fasstr_calc_longterm_daily_stats /
-- fasstr_compute_frequency_quantile without this - included anyway for
-- explicitness/defense against someone later REVOKEing the PUBLIC default.
grant all on all functions in schema fasstr to "${appUser}";
alter default privileges in schema fasstr grant execute on functions to "${appUser}";

grant usage on schema postgis_ftw to ftw_reader;
alter default privileges in schema postgis_ftw grant select on tables to ftw_reader;