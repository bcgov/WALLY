from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from sqlalchemy.orm import Session
from fastapi import Depends
from logging import getLogger
from api.db.utils import get_db
from api.v1.user.db_models import User

logger = getLogger('auth')


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request, db: Session = Depends(get_db)):
        # This application sits behind an auth service Keycloak Gatekeeper, so we don't really
        # need to authenticate here. We just need to log the authenticated user's data to make
        # sure we have a matching user in the database.
        if "X-Auth-Subject" not in request.headers:
            return

        sub = request.headers['X-Auth-Subject']
        email = request.headers['X-Auth-Email']
        roles = request.headers['x-auth-roles']
        userid = request.headers['x-auth-userid']

        logger.info(sub, email, roles, userid)

        user = User.get_or_create(db, sub)

        # Update user email
        user.email = email
        db.commit()

        # update_user = False
        # if user.email != email:
        #     update_user = True
        #     user.email = email
        #
        # if user.user_idir != userid:
        #     update_user = True
        #     user.user_idir = userid
        #
        # if update_user:
        #     user.save()

        # return AuthCredentials(["authenticated"])
        return AuthCredentials(["authenticated"]), user
