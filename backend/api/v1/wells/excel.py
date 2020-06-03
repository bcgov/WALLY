from typing import List
import logging
import datetime
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
    ws = wb.active
    ws.title = "well"

    # testing whether headers have been created
    # lists so we can pass by reference to append method
    ls_set = [False]
    cs_set = [False]
    ss_set = [False]
    ps_set = [False]
    dls_set = [False]
    dvs_set = [False]

    # create the other well information sheets
    ls = wb.create_sheet("lithology")
    cs = wb.create_sheet("casing")
    ss = wb.create_sheet("screen")
    ps = wb.create_sheet("perforation")
    dls = wb.create_sheet("drilling_method")
    dvs = wb.create_sheet("development_method")

    # set well sheet headers
    well_headers = [*features[0].geojson.features[0].properties]
    ws.append(well_headers)

    for dataset in features:
        # avoid trying to process layers if they have no features.
        if not dataset.geojson:
            continue
        
        # set well information first then subset list data
        try:
            props = dataset.geojson.features[0].properties
            
            well = props
            well_tag_number = props["well_tag_number"]
            if well:
                ws.append([str(i) for i in list(well.values())])
            
            append_sheet_values(props["lithologydescription_set"], ls_set, ls, well_tag_number)
            append_sheet_values(props["casing_set"], cs_set, cs, well_tag_number)
            append_sheet_values(props["screen_set"], ss_set, ss, well_tag_number)
            append_sheet_values(props["linerperforation_set"], ps_set, ps, well_tag_number)
            append_sheet_values(props["drilling_methods"], dls_set, dls, well_tag_number)

            # drilling_methods is a string array so we handle it explicitly
            if props["development_methods"]:
                if not dvs_set[0]:
                    dvs.append(["well_tag_number", "development_method"])
                    dvs_set[0] = True
                for item in props["development_methods"]:
                    dvs.append([well_tag_number, str(item)])

        except Exception as e:
            logger.warn(e)
            continue

    cur_date = datetime.datetime.now().strftime("%X-%Y-%m-%d")
    filename = f"{cur_date}_CrossSection"

    response = Response(
        content=save_virtual_workbook(wb),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={filename}.xlsx'})

    return response


def append_sheet_values(value_set, isSet, sheet, well_tag_number):
    """
      Check if any subset data exists and if so
      add it to the appropriate xls sheet.
      If the isSet bool is False then we add
      headers for that sheet first.
      Well tag number is concated to the front
      of the list on each row.
    """
    if value_set:
        if not isSet[0]:
            sheet.append(["well_tag_number"] + [str(i) for i in value_set[0]])
            isSet[0] = True
        for item in value_set:
            sheet.append([well_tag_number] + [str(i) for i in list(item.values())])
