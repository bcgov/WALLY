from sqlalchemy.ext.declarative import declarative_base, declared_attr


class CustomBase(object):
    pass


BaseTable = declarative_base(cls=CustomBase)
