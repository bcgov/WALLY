from api.config import AUTH_WELL_KNOWN_ENDPOINT, AUTH_CLIENT
import jwt
import requests
import json
import logging

logger = logging.getLogger()

def validate_token(token):
    try:
        token_decoded = None
        oidc_response = requests.get(AUTH_WELL_KNOWN_ENDPOINT)
        jwks_uri = json.loads(oidc_response.text)['jwks_uri']
        jwks_client = jwt.PyJWKClient(jwks_uri)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        token_decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUTH_CLIENT,
            options={"verify_exp": True},
        )
    except Exception as ex:
            logger.error(ex) 
            print(ex)  
    return token_decoded


def user_authorized(token_dict):
    return (token_dict["aud"] == AUTH_CLIENT and 
           token_dict["identity_provider"] == 'idir' and 
           "client_roles" in token_dict and 'wally-view' in token_dict["client_roles"])