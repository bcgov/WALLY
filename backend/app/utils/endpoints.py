from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException
import pdfkit
from app import config
from starlette.responses import Response

logger = getLogger("utils")

router = APIRouter()d


@router.get("/report")
def generate_report():
    logger.info('getting report from')
    logger.info(config.REPORT_URL)
    pdf_report = pdfkit.from_url(config.REPORT_URL, False)

    response = Response(
        content=pdf_report,
        media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=report.pdf'})
    return response
