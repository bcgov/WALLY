import requests
import base64
from api import config

def get_docgen_token():
    params = {
        "grant_type": "client_credentials",
        "scope": ""
    }

    auth_string = f"{config.COMMON_DOCGEN_CLIENT_ID}:{config.COMMON_DOCGEN_CLIENT_SECRET}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_auth}"
    }

    req = requests.post(
        config.COMMON_DOCGEN_SSO_ENDPOINT,
        data=params,
        headers=headers
    )
    req.raise_for_status()

    resp = req.json()

    token = resp.get('access_token')
    return token