# Import all the models, so that Base has them before being
# imported by Alembic
from api.db.base_class import BaseTable, BaseLayerTable  # noqa
import api.v1.hydat.db_models
import api.v1.catalogue.db_models
import api.v1.models.scsb2016.db_models
import api.layers.automated_snow_weather_station_locations
import api.layers.bc_major_watersheds
import api.layers.bc_wildfire_active_weather_stations
import api.layers.automated_snow_weather_station_locations
import api.layers.cadastral
import api.layers.critical_habitat_species_at_risk
import api.layers.ecocat_water_related_reports
import api.layers.first_nations
import api.layers.freshwater_atlas_stream_directions
import api.layers.freshwater_atlas_stream_networks
import api.layers.freshwater_atlas_watersheds
import api.layers.ground_water_aquifers
import api.layers.ground_water_wells
import api.layers.normal_annual_runoff_isolines
import api.layers.water_allocation_restrictions
import api.layers.water_rights_applications
import api.layers.water_rights_licences
import api.v1.user.db_models