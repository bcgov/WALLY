import logging
from fastapi import APIRouter, Depends, HTTPException
import pdfkit
from app import config
from starlette.responses import Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("utils")

router = APIRouter()


@router.get("/report")
def generate_report():
    logger.info(f"getting report from {config.REPORT_URL}")
    pdf_report = pdfkit.from_url(config.REPORT_URL, False)

    logger.info(f"pdf: ", pdf_report)

    response = Response(
        content=pdf_report,
        media_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=report.pdf'})
    return response
