from typing import List
import logging
import datetime
import openpyxl
from openpyxl.writer.excel import save_virtual_workbook
from starlette.responses import Response
from geojson import FeatureCollection
from api.v1.aggregator.schema import LayerResponse

logger = logging.getLogger('well export')


def crossSectionXlsxExport(features: List[LayerResponse], coordinates: list, buffer: int):
    """
    packages features into an excel workbook.  Returns an HTTP response object that has the saved workbook
    ready to be returned to the client (e.g. the calling http handler can return this object directly)
    """

    workbook = openpyxl.Workbook()
    details_sheet = workbook.active
    details_sheet.title = "details"

    # create data sheets
    well_sheet = workbook.create_sheet("well")
    lith_sheet = workbook.create_sheet("lithology")
    screen_sheet = workbook.create_sheet("screen")

    cur_date = datetime.datetime.now().strftime("%X-%Y-%m-%d")

    # details tab
    details_headers = ['title', 'date', 'A latitude', 'A longitude', 'B latitude', 'B longitude', 'buffer radius (m)']
    details_sheet.append(details_headers)
    details_sheet.append(['Cross Section Analysis', cur_date, str(coordinates[0][1]), str(coordinates[0][0]), str(coordinates[1][1]), str(coordinates[1][0]), buffer])

    # data sheet headers added
    well_sheet.append(WELL_HEADERS)
    lith_sheet.append(LITHOLOGY_HEADERS)
    screen_sheet.append(SCREEN_HEADERS)

    for dataset in features:
        # avoid trying to process layers if they have no features.
        if not dataset.geojson:
            continue
        
        # set row information
        try:
            props = dataset.geojson.features[0].properties
            well_tag_number = props["well_tag_number"]

            well_values = [props.get(x, None) for x in WELL_HEADERS]
            well_sheet.append(well_values)

            lith_set = props["lithologydescription_set"]
            logger.warn(lith_set)
            for item in lith_set:
                lith_values = [item.get(x, None) for x in LITHOLOGY_INDEX]
                lith_sheet.append([well_tag_number] + lith_values)

            screen_set = props["screen_set"]
            logger.warn(screen_set)
            for item in screen_set:
                screen_values = [item.get(x, None) for x in SCREEN_INDEX]
                screen_sheet.append([well_tag_number] + screen_values)

        except Exception as e:
            logger.warn(e)
            continue

    filename = f"{cur_date}_CrossSection"

    response = Response(
        content=save_virtual_workbook(workbook),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={filename}.xlsx'})

    return response


SCREEN_INDEX = [
    'start',
    'end',
    'diameter',
    'assembly_type',
    'slot_size'
]

SCREEN_HEADERS = [
    'well_tag_number',
    'screen_from',
    'screen_to',
    'screen_diameter',
    'screen_assembly_type',
    'screen_slot_size'
]

LITHOLOGY_INDEX = [
    'start',
    'end',
    'lithology_raw_data',
    'lithology_description',
    'lithology_material',
    'lithology_hardness',
    'lithology_colour',
    'water_bearing_estimated_flow',
    'lithology_observation'
]

LITHOLOGY_HEADERS = [
    'well_tag_number',
    'lithology_from',
    'lithology_to',
    'lithology_raw_data',
    'lithology_description_code',
    'lithology_material_code',
    'lithology_hardness_code',
    'lithology_colour_code',
    'water_bearing_estimated_flow',
    'lithology_observation'
]

WELL_HEADERS = [
    "well_tag_number",
    "identification_plate_number",
    "well_identification_plate_attached",
    "well_status",
    "well_class",
    "well_subclass",
    "intended_water_use",
    "licenced_status",
    "observation_well_number",
    "obs_well_status",
    "water_supply_system_name",
    "water_supply_system_well_name",
    "street_address",
    "city",
    "legal_lot",
    "legal_plan",
    "legal_district_lot",
    "legal_block",
    "legal_section",
    "legal_township",
    "legal_range",
    "land_district",
    "legal_pid",
    "well_location_description",
    "latitude",
    "longitude",
    "utm_zone",
    "utm_northing",
    "utm_easting",
    "owner_full_name",
    "well_publication_status",
    "construction_start_date",
    "construction_end_date",
    "alteration_start_date",
    "alteration_end_date",
    "decommission_start_date",
    "decommission_end_date",
    "coordinate_acquisition",
    "ground_elevation",
    "ground_elevation_method",
    "other_screen_material",
    "other_screen_bottom",
    "screen_information",
    "total_depth_drilled",
    "finished_well_depth",
    "final_casing_stick_up",
    "bedrock_depth",
    "static_water_level",
    "artesian_flow",
    "artesian_pressure",
    "comments",
    "well_yield",
    "well_yield_unit",
    "diameter",
    "ems",
    "aquifer_id",
    "aquifer_vulnerability_index",
    "aquifer_lithology",
    "storativity",
    "transmissivity",
    "hydraulic_conductivity",
    "specific_storage",
    "specific_yield",
    "testing_method",
    "testing_duration",
    "analytic_solution_type",
    "boundary_effect",
    "drawdown",
    "recommended_pump_depth",
    "surface_seal_material",
    "surface_seal_method",
    "liner_material",
    "screen_intake_method",
    "screen_type",
    "screen_material",
    "screen_opening",
    "screen_bottom",
    "avi"
]
