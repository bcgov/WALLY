import logging
from fastapi import APIRouter, Depends, HTTPException
import pdfkit
from app import config
from starlette.responses import FileResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("utils")

router = APIRouter()


@router.get("/report")
def generate_report():
    logger.info(f"getting report from {config.REPORT_URL}")

    temp_file = '/tmp/report.pdf'
    pdfkit.from_url(config.REPORT_URL, temp_file)

    logger.info(f"Saved to {temp_file}")

    response = FileResponse(
        path=temp_file,
        media_type="application/pdf",
        filename='report.pdf')

    # response = Response(
    #     content=pdf_report,
    #     media_type='application/pdf',
    #     headers={'Content-Disposition': 'attachment; filename=report.pdf'})
    return response
