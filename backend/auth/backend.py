from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, UnauthenticatedUser,
    AuthCredentials
)
from logging import getLogger

logger = getLogger('auth')


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        logger.info("auth------")
        logger.info(request)
        logger.info("auth_headers----")
        logger.info(request.headers)

        if "X-Auth-Subject" not in request.headers:
            return

        return AuthCredentials(["authenticated"])
