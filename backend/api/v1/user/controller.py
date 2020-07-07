import json
import logging
from sqlalchemy import text, func
from sqlalchemy.orm import Session
from api.v1.user.db_models import User
from datetime import datetime

logger = logging.getLogger("user")


def get_create_user(db: Session, uuid):
    """ get or create user based on uuid pk """

    user = db.query(User).filter(User.uuid == uuid).first()
    if not user:
        date = datetime.now()
        user = User(
            uuid=uuid,
            create_date=date,
            update_date=date
        )
        db.add(user)
        db.commit()

    logger.warning(user)
    return user


def update_map_layers(db: Session, user):
    """ updates user default map layers from string array """
    db.query(User).filter(User.uuid == user.uuid) \
      .update({User.default_map_layers: user.map_layers})
    db.commit()
    logger.warning(user)
    return True
