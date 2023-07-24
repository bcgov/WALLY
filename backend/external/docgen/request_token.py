import requests
import base64
from api import config
from fastapi import HTTPException
import logging

logger = logging.getLogger('docgen')

def get_docgen_token():
    params = {
        "grant_type": "client_credentials"
    }

    auth_string = f"{config.COMMON_DOCGEN_CLIENT_ID}:{config.COMMON_DOCGEN_CLIENT_SECRET}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}"
    }

    logger.info('making POST request to common docgen sso endpoint: %s',
                config.COMMON_DOCGEN_SSO_ENDPOINT)

    try:
        res = requests.post(
            config.COMMON_DOCGEN_SSO_ENDPOINT,
            data=params,
            headers=headers)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.info(e)
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    return res.json().get('access_token')