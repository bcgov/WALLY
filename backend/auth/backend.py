from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from sqlalchemy.orm import Session
from fastapi import Depends
from logging import getLogger
from api.db.utils import get_db_session
from api.v1.user.db_models import User
from api.config import WALLY_ENV, ENV_DEV
from api.config import get_settings

logger = getLogger('auth')


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        # This application sits behind an auth service Keycloak Gatekeeper, so we don't really
        # need to authenticate here. We just need to log the authenticated user's data to make
        # sure we have a matching user in the database.
        if "X-Auth-Subject" not in request.headers and WALLY_ENV != ENV_DEV:
            raise AuthenticationError("OIDC Subject (User) not found")

        # Skip for unit tests and kube-prob
        if 'testclient' == request.headers['user-agent'] or \
                'kube-probe' in request.headers['user-agent']:
            return

        settings = get_settings()

        if WALLY_ENV == ENV_DEV and settings.local_development:
            # Dev user
            sub = '00000000-0000-0000-0000-000000000000'
            email = 'dev.wally.test@gov.bc.ca'
            roles = ''
            userid = 'dev@idir'
        else:
            sub = request.headers['x-auth-subject']
            email = request.headers['x-auth-email']
            roles = request.headers['x-auth-roles']
            userid = request.headers['x-auth-userid']

        db = get_db_session()

        user = User.get_or_create(db, sub)

        update_user = False
        # if user.email != email:
        #     update_user = True
        #     user.email = email

        if user.user_idir != userid:
            update_user = True
            user.user_idir = userid

        if update_user:
            db.commit()

        # return AuthCredentials(["authenticated"])
        return AuthCredentials(["authenticated"]), user
