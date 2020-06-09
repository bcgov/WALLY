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
    # cs_set = [False]
    ss_set = [False]
    # ps_set = [False]
    # dls_set = [False]
    # dvs_set = [False]

    # Create Sheets
    dt = wb.create_sheet("details")
    ls = wb.create_sheet("lithology")
    ss = wb.create_sheet("screen")
    # ps = wb.create_sheet("perforation")
    # dls = wb.create_sheet("drilling_method")
    # dvs = wb.create_sheet("development_method")

    # Set Headers
    detail_headers = ['title', 'date', 'A coordinates', 'B coordinates', 'buffer radius (m)', 'off-set line']
    dt.append(detail_headers)

    # well_headers = [*features[0].geojson.features[0].properties]
    well_headers = ["well_tag_number",	"identification_plate_number",	"well_identification_plate_attached",	"well_status_code",	"well_class_code", "well_subclass",	"intended_water_use_code",	"licenced_status_code",	"observation_well_number",	"obs_well_status_code",	"water_supply_system_name",	"water_supply_system_well_name",	"street_address",	"city",	"legal_lot",	"legal_plan",	"legal_district_lot",	"legal_block",	"legal_section",	"legal_township",	"legal_range",	"land_district_code",	"legal_pid",	"well_location_description",	"latitude",	"longitude",	"utm_zone_code",	"utm_northing",	"utm_easting",	"coordinate_acquisition_code", 	"construction_start_date",	"construction_end_date",	"alteration_start_date",	"alteration_end_date",	"decommission_start_date",	"decommission_end_date", "diameter",	"total_depth_drilled",	"finished_well_depth",	"final_casing_stick_up",	"bedrock_depth",	"ground_elevation",	"ground_elevation_method_code",	"static_water_level",	"well_yield",	"well_yield_unit_code",	"artesian_flow",	"artesian_pressure",	 "well_disinfected_code", 	"surface_seal_material_code",	"surface_seal_method_code",				"liner_material_code",						"screen_intake_method_code",	"screen_type_code",	"screen_material_code",	"other_screen_material",	"screen_information",	"screen_opening_code",	"screen_bottom_code",	"other_screen_bottom", "filter_pack_material_code", "filter_pack_material_size_code",	"yield_estimation_method_code",	"drawdown",	"decommission_method_code",	"comments",	"ems", "aquifer_id",	"avi",	"storativity",	"transmissivity",	"hydraulic_conductivity",	"specific_storage",	"specific_yield",	"testing_method",	"testing_duration",	"analytic_solution_type",	"boundary_effect_code",	"aquifer_lithology_code"]
    ws.append(well_headers)

    lithology_headers = ['well_tag_number', 'lithology_from', 'lithology_to', 'lithology_raw_data', 'lithology_description_code', 'lithology_material_code', 'lithology_hardness_code', 'lithology_colour_code', 'water_bearing_estimated_flow','lithology_observation']
    ls.append(lithology_headers)

    screen_headers = ['screen_from', 'screen_to', 'screen_diameter', 'screen_assembly_type', 'screen_slot_size']
    ss.append(screen_headers)

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
            # append_sheet_values(props["casing_set"], cs_set, cs, well_tag_number)
            append_sheet_values(props["screen_set"], ss_set, ss, well_tag_number)
            # append_sheet_values(props["linerperforation_set"], ps_set, ps, well_tag_number)
            # append_sheet_values(props["drilling_methods"], dls_set, dls, well_tag_number)

            # development_methods is a string array so we handle it explicitly
            # if props["development_methods"]:
            #     if not dvs_set[0]:
            #         dvs.append(["well_tag_number", "development_method"])
            #         dvs_set[0] = True
            #     for item in props["development_methods"]:
            #         dvs.append([well_tag_number, str(item)])

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
      Well tag number is concatenated to the
      front of the list on each row.
    """
    if value_set:
        if not isSet[0]:
            sheet.append(["well_tag_number"] + [str(i) for i in value_set[0]])
            isSet[0] = True
        for item in value_set:
            sheet.append([well_tag_number] + [str(i) for i in list(item.values())])
