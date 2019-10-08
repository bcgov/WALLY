# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import BaseTable  # noqa
from app.hydat.db_models import Station
from app.metadata.db_models import DisplayCatalogue, LayerCategory
