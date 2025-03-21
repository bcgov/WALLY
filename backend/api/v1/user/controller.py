import uuid
import logging
from sqlalchemy.orm import Session
from api.v1.user.db_models import UserMapLayer, User
from datetime import datetime

logger = logging.getLogger("user")


def get_create_user_map_layer(db: Session, user_idir):
    """ get or create user map layer based on idir """

    user_map_layer = db.query(UserMapLayer).filter(UserMapLayer.user_idir == user_idir).first()
    if not user_map_layer:
        date = datetime.now()
        user_map_layer = UserMapLayer(
            user_idir=user_idir,
            create_date=date,
            update_date=date
        )
        db.add(user_map_layer)
        db.commit()

    return user_map_layer


def update_map_layers(db: Session, user, map_layers):
    """ updates user default map layers from string array """

    db.query(UserMapLayer).filter(UserMapLayer.user_idir == user.user_idir) \
        .update({UserMapLayer.default_map_layers: map_layers})

    db.commit()

    return True
