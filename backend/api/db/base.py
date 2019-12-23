# Import all the models, so that Base has them before being
# imported by Alembic
from api.db.base_class import BaseTable, BaseLayerTable  # noqa
from api.v1.hydat.db_models import Station
from api.metadata.db_models import DisplayCatalogue, LayerCategory
