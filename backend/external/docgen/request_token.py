import requests
from api import config


def get_docgen_token():
    params = {
        "grant_type": "client_credentials",
        "client_id": config.COMMON_DOCGEN_CLIENT_ID,
        "client_secret": config.COMMON_DOCGEN_CLIENT_SECRET,
        "scope": ""
    }

    req = requests.post(
        config.COMMON_DOCGEN_SSO_ENDPOINT,
        data=params,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )
    req.raise_for_status()

    resp = req.json()

    token = req.json().get('access_token')
    return token
