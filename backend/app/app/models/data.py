from pydantic import BaseModel, BaseConfig
from geoalchemy2 import WKTElement


class DataSourceBase(BaseModel):
    """ Not a database. """
    title: str = None
    description: str = None


# Properties shared by models stored in DB
class DataSourceInDBBase(DataSourceBase):
    id: str
    name: str
    type: str
    api_uri: str
    web_uri: str
    coordinates: WKTElement

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class DataSource(DataSourceInDBBase):
    pass


# Properties properties stored in DB
class DataSourceInDB(DataSourceInDBBase):
    pass
