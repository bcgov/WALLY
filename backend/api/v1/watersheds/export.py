""" Functions for exporting watershed data in alternate (non-JSON) formats """
import datetime
import fiona
import io
import os
import zipfile

from fastapi import Response
from tempfile import TemporaryDirectory
from shapely.geometry import Polygon, mapping
from external.docgen.controller import docgen_export_to_xlsx
from external.docgen.templates import SURFACE_WATER_XLSX_TEMPLATE


def export_summary_as_xlsx(data: dict):
    """ exports watershed summary data as an excel file
        using a template in the ./templates directory.
    """

    cur_date = datetime.datetime.now().strftime("%Y%m%d")

    ws_name = data.get("watershed_name", "Surface_Water")
    ws_name.replace(" ", "_")

    filename = f"{cur_date}_{ws_name}"

    excel_file = docgen_export_to_xlsx(
        data, SURFACE_WATER_XLSX_TEMPLATE, filename)

    return Response(
        content=excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}.xlsx"}
    )


def export_summary_as_shapefile(data: dict, geom: Polygon):
    """exports watershed summary data as a shapefile"""

    cur_date = datetime.datetime.now().strftime("%Y%m%d")

    ws_name = data.get("watershed_name", "Surface_Water")
    ws_name.replace(" ", "_")

    filename = f"{cur_date}_{ws_name}"

    # Schema for watershed data
    poly_schema = {
        'geometry': 'Polygon',
        'properties': {
            'name': 'str'
        },
    }

    with TemporaryDirectory() as tmpdir:
        watershed_file = f"{tmpdir}/watershed.shp"
        # New shapefile for the watershed data.
        with fiona.open(watershed_file, 'w', 'ESRI Shapefile', poly_schema, crs=f"EPSG:4326") as c:
            c.write({
                'geometry': mapping(geom),
                'properties': {
                    'name': ws_name
                },
            })

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for f in os.listdir(tmpdir):
                zip_file.write(f)

    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}.xlsx"}
    )
