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
        # Skip for unit tests and kube-prob
        if 'testclient' == request.headers['user-agent'] or \
                'kube-probe' in request.headers['user-agent']:
            return

        token = request.headers['token']

        if "token" not in request.headers and WALLY_ENV != ENV_DEV:
            raise AuthenticationError("OIDC Subject (User) not found")

        settings = get_settings()
        if WALLY_ENV == ENV_DEV and settings.local_development:
            # Dev user
            sub = '00000000-0000-0000-0000-000000000000'
            email = 'dev.wally.test@gov.bc.ca'
            roles = ''
            userid = 'dev@idir'
        else:
            sub = token.sub
            email = token.email
            roles = token.client_roles
            userid = token.idir_username

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
