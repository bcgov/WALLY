from typing import List
import logging
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook
from starlette.responses import Response
from geojson import FeatureCollection
from api.v1.aggregator.schema import LayerResponse

logger = logging.getLogger('well export')


def crossSectionXlsxExport(features: List[LayerResponse]):
    """
    packages features into an excel workbook.  Returns an HTTP response object that has the saved workbook
    ready to be returned to the client (e.g. the calling http handler can return this object directly)
    """

    wb = openpyxl.Workbook()
    well = wb.active
    well.title = "well"

    # create the other well information sheets
    lithology = wb.create_sheet("lithology")
    casing = wb.create_sheet("casing")
    screen = wb.create_sheet("screen")
    perforation = wb.create_sheet("perforation")
    drilling_method = wb.create_sheet("drilling_method")
    development_method = wb.create_sheet("development_method")

    logger.warn(features)
    logger.warn(features[0].geojson.features[0].properties)
    
    well_headers = [*features[0].geojson.features[0].properties]
    well.append(well_headers)

    for dataset in features:
        # avoid trying to process layers if they have no features.
        if not dataset.geojson:
            continue

        # create a list of fields for this dataset
        fields = []
        try:
            p = dataset.geojson.features[0].properties
            
            well.append([str(i) for i in list(p.values())])


            lithology.append([str(i) for i in list(p.lithologydescription_set.values())])
            
            
            casing.append([str(i) for i in list(p.casing_set.values())])
            screen.append([str(i) for i in list(p.screen_set.values())])
            perforation.append([str(i) for i in list(p.linerperforation_set.values())])
            drilling_method.append([str(i) for i in list(p.drilling_methods.values())])
            development_method.append([str(i) for i in list(p.development_methods.values())])
            
            # fields = list(dataset.geojson.features[0].properties.values())
            # fields = [str(i) for i in fields]
        except:
            continue
        
        # logger.warn(fields)
        # well.append(fields)
        # lithology.append()
        # casing.append()
        # screen.append()
        # perforation.append()
        # drilling_method.append()
        # development_method.append()

        # features = dataset.geojson.features
        # # add rows for every object in the collection, using the fields defined above.
        # for f in features:
        #     props = f['properties']
        #     ws.append([
        #         props.get(x) for x in fields
        #     ])

    response = Response(
        content=save_virtual_workbook(wb),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=report.xlsx'})

    return response


def geojson_to_xlsx(fc_list: List[FeatureCollection], filename: str = "report"):
    """
    packages a list of FeatureCollections into an excel workbook.
    Each FeatureCollection will get its own sheet/tab in the workbook.

    Returns an HTTP response object that has the saved workbook
    ready to be returned to the client (e.g. the calling http handler can return this object directly)
    """

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    first_sheet = True

    for i, fc in enumerate(fc_list, start=1):
        # avoid trying to process layers if they have no features.
        if not fc.features:
            continue

        # create a list of fields for this dataset
        fields = []
        try:
            fields = [*fc.features[0].properties]
        except:
            continue

        sheet_title = fc.properties['name'] or fc.properties['layer'] or f"sheet {i}"

        if not first_sheet:
            worksheet = workbook.create_sheet(sheet_title)
        else:
            worksheet.title = sheet_title
            first_sheet = False

        worksheet.append(fields)

        # add rows for every object in the collection, using the fields defined above.
        for f in fc.features:
            props = f['properties']
            worksheet.append([
                props.get(x) for x in fields
            ])

    response = Response(
        content=save_virtual_workbook(workbook),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={filename}.xlsx'})

    return response
