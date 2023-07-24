""" Functions for interacting with the Common Document Generator (CDOGS) API  """

import base64
import requests
import logging
import os 

from fastapi import HTTPException

from api import config

from external.docgen.request_token import get_docgen_token
from external.docgen.schema import DocGenRequest, DocGenOptions, DocGenTemplateFile

logger = logging.getLogger('docgen')


def docgen_export_to_xlsx(data, template_path, report_name):
    """ accepts a data dict and a path to an xlsx template
        and makes a request to CDOGS.
        Returns the response content object that can be added to a 
        starlette.responses.Response.

    """

    token = get_docgen_token()
    auth_header = f"Bearer {token}"

    template_file_path = os.path.join('/app', template_path)
    with open(template_file_path, "rb") as template_file:
        template_data = template_file.read()
    base64_encoded = base64.b64encode(template_data).decode("UTF-8")

    body = DocGenRequest(
        data=data,
        options=DocGenOptions(
            reportName=report_name,
        ).dict(),
        template=DocGenTemplateFile(
            encodingType="base64",
            content=base64_encoded,
            fileType="xlsx"
        ).dict()
    )

    logger.info('making POST request to common docgen: %s',
                config.COMMON_DOCGEN_ENDPOINT)

    try:
        res = requests.post(config.COMMON_DOCGEN_ENDPOINT, json=body.dict(), headers={
                            "Authorization": auth_header, "Content-Type": "application/json"})
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.info(e)
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

    return res.content
