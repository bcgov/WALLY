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
from auth.sso import validate_token, user_authorized


logger = getLogger('auth')


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        # Skip for unit tests and kube-prob
        if 'testclient' == request.headers['user-agent'] or \
                'kube-probe' in request.headers['user-agent']:
            return

        token = request.headers['token']

        if "token" not in request.headers and WALLY_ENV != ENV_DEV:
            raise AuthenticationError("OIDC Subject (User) not found", )

        settings = get_settings()

        token_decoded = validate_token(token)
        if token_decoded == None:
            raise AuthenticationError("AuthError")

        if WALLY_ENV == ENV_DEV and settings.local_development:
            # Dev user
            idir_user_guid = '00000000-0000-0000-0000-000000000000'
            userid = 'dev'
        else:
            if user_authorized(token_decoded):
                pass
            else:
                logger.error("The user does not have permission to use this application") 
                raise AuthenticationError("NotAuthorized")
        
        idir_user_guid = token_decoded["idir_user_guid"]
        userid = token_decoded["idir_username"]

        db = get_db_session()

        user = User.get_or_create(db, idir_user_guid)

        update_user = False

        if user.user_idir != userid:
            update_user = True
            user.user_idir = userid

        if update_user:
            db.commit()

        # return AuthCredentials(["authenticated"])
        return AuthCredentials(["authenticated"]), user
