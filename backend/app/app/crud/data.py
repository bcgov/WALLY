from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db_models.data import DataSource


def get_multi(db_session: Session) -> List[Optional[DataSource]]:
    return db_session.query(DataSource).all()
