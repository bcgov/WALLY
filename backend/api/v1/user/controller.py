from fastapi import HTTPException
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.v1.user.db_models import User
from datetime import datetime

logger = logging.getLogger("user")


def get_create_user(db: Session, user_id):
    """ get or create user based on uuid pk """

    user = db.query(User).filter(User.uuid == user_id).first()
    if not user:
        date = datetime.now()
        user = User(
            uuid=user_id,
            create_date=date,
            update_date=date
        )
        db.add(user)
        db.commit()

    return user


def update_map_layers(db: Session, user_id, map_layers):
    """ updates user default map layers from string array """
    db.query(User).filter(User.uuid == user_id) \
      .update({User.default_map_layers: map_layers})
    db.commit()

    return True


def validate_user(db: Session, user_id: str):
    # validate user
    user = db.query(func.count(User.uuid)).filter(User.uuid == user_id).scalar()
    if user == 0:
        raise HTTPException(status_code=422, detail="Invalid user")
