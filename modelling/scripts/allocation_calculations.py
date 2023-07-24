from numpy.core.records import record
import pandas as pd
import csv
import json
import ast

# station_number,most_recent_year,years_of_data,mean,min,max,drainage_area_gross,latitude,longitude,gen_id,annual_precipitation,aspect,average_slope,drainage_area,glacial_area,glacial_coverage,hydrological_zone,median_elevation,potential_evapotranspiration,solar_exposure,watershed_area
df_stats = pd.read_csv("../data/2_scrape_results/july30_licence_data/watershed_stats_output.csv")

# station_number, gen_id, approvals, total_qty, projected_geometry_area, projected_geometry_area_simplified
df_approvals = pd.read_csv("../data/2_scrape_results/july30_licence_data/watershed_approvals_output.csv")

# station_number, gen_id, licences, inactive_licencese, total_qty, total_qty_by_purpose, projected_geometry_area, projected_geometry_area_simplified
df_licences = pd.read_csv("../data/2_scrape_results/july30_licence_data/watershed_licence_output.csv")

# Purpose_Num, Consumptive?, Purpose, Units, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Sum, PREVIOUS_monthly_coefficients, Description of Water License Purpose, Reference/Note
df_allocation_coef = pd.read_csv("../data/2_scrape_results/july30_licence_data/monthly_allocation_coefficients.csv")

# Purpose_Num, Consumptive?, Purpose, Units, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Sum, Reference
df_return_coef = pd.read_csv("../data/2_scrape_results/july30_licence_data/monthly_return_coefficients.csv")

# PURPOSE_USE_CODE == Purpose_Num

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


def normalize_quantity(qty, qty_unit: str):
    """ takes a qty and a unit (as a string) and returns the quantity in m3/year
        accepts:
        m3/sec
        m3/day
        m3/year
        Returns None if QUANTITY_UNITS doesn't match one of the options.
    """
    if qty_unit is None:
        return None

    qty_unit = qty_unit.strip()

    if qty_unit == 'm3/year':
        return qty
    elif qty_unit == 'm3/day':
        return qty * 365
    elif qty_unit == 'm3/sec':
        return qty * 60 * 60 * 24 * 365
    else:
        # could not interpret QUANTITY_UNIT value
        return None


def compute_monthly_allocations(qty, allocations):
    allocated_values = {}
    for month in MONTHS:
        allocated_values[month] = 0

    alloc_sum = allocations['Sum']

    for month in MONTHS:
        try:
            if alloc_sum > 0:
                allocated_values[month] = qty * allocations[month] / alloc_sum
            else: 
                allocated_values[month] = 0
        except:
            print('error on allocated values', qty, allocations[month], alloc_sum)
    # print(allocated_values)
    return allocated_values


def compute_station_quantities():
    for index, station in df_stats.iterrows():
        station_number = station['station_number']
        licence_records = df_licences.loc[df_licences['station_number'] == station_number]
        approval_records = df_approvals.loc[df_approvals['station_number'] == station_number]
        
        # totals variables
        total_licenced_qty = 0
        total_monthly_licenced_qtys = {}
        total_monthly_return_qtys = {}
        total_monthly_absolute_qtys = {}
        for month in MONTHS:
            total_monthly_licenced_qtys[month] = 0
            total_monthly_return_qtys[month] = 0
            total_monthly_absolute_qtys[month] = 0

        # licences allocation/return
        for index, licence_record in licence_records.iterrows():
            licences = licence_record['licences']
            licences = json.dumps(ast.literal_eval(licences))
            licences = json.loads(licences)
            licences = licences['features']

            for licence in licences:
                properties = licence['properties']
                purpose_use_code = properties['PURPOSE_USE_CODE']
                qty_m3_yr = properties['qty_m3_yr']
                if qty_m3_yr is None:
                    qty_m3_yr = 0

                allocation_coef = df_allocation_coef.loc[df_allocation_coef['Purpose_Num'] == purpose_use_code]
                allocation_coef = allocation_coef[MONTHS + ['Sum']].to_dict('records')[0]
                monthly_allocations = compute_monthly_allocations(qty_m3_yr, allocation_coef)

                return_coef = df_return_coef.loc[df_return_coef['Purpose_Num'] == purpose_use_code]
                return_coef = return_coef[MONTHS + ['Sum']].to_dict('records')[0]
                monthly_returns = compute_monthly_allocations(qty_m3_yr, return_coef)

                # add up licence variables
                total_licenced_qty += qty_m3_yr
                for month in MONTHS:
                    total_monthly_licenced_qtys[month] += monthly_allocations[month]
                    total_monthly_return_qtys[month] += monthly_returns[month]
                    total_monthly_absolute_qtys[month] += monthly_allocations[month] - monthly_returns[month]

        # print(total_monthly_licenced_qtys)
        # print(total_monthly_return_qtys)
        # print(total_monthly_absolute_qtys)

        total_approval_qty = 0
        total_approval_monthly_licenced_qtys = {}
        total_approval_monthly_return_qtys = {}
        total_approval_monthly_absolute_qtys = {}
        for month in MONTHS:
            total_approval_monthly_licenced_qtys[month] = 0
            total_approval_monthly_return_qtys[month] = 0
            total_approval_monthly_absolute_qtys[month] = 0

        # approvals allocation/return
        for index, approval_record in approval_records.iterrows():
            approvals = approval_record['approvals']
            approvals = json.dumps(ast.literal_eval(approvals))
            approvals = json.loads(approvals)
            approvals = approvals['features']

            for approval in approvals:
                properties = approval['properties']
                purpose_use_code = properties['APPROVAL_TYPE']
                if purpose_use_code != ['STU']:
                    continue

                qty_m3_yr = normalize_quantity(properties['QUANTITY'], properties['QUANTITY_UNITS'])
                if qty_m3_yr is None:
                    qty_m3_yr = 0

                allocation_coef = df_allocation_coef.loc[df_allocation_coef['Purpose_Num'] == purpose_use_code]
                allocation_coef = allocation_coef[MONTHS + ['Sum']].to_dict('records')[0]
                monthly_allocations = compute_monthly_allocations(qty_m3_yr, allocation_coef)

                return_coef = df_return_coef.loc[df_return_coef['Purpose_Num'] == purpose_use_code]
                return_coef = return_coef[MONTHS + ['Sum']].to_dict('records')[0]
                monthly_returns = compute_monthly_allocations(qty_m3_yr, return_coef)

                # add up approval variables
                total_approval_qty += qty_m3_yr
                for month in MONTHS:
                    total_approval_monthly_licenced_qtys[month] += monthly_allocations[month]
                    total_approval_monthly_return_qtys[month] += monthly_returns[month]
                    total_approval_monthly_absolute_qtys[month] += monthly_allocations[month] - monthly_returns[month]

        # print(total_approval_monthly_licenced_qtys)
        # print(total_approval_monthly_return_qtys)
        # print(total_approval_monthly_absolute_qtys)

        total_qty = {}
        total_return = {}
        total_absolute = {}
        for month in MONTHS:
            total_qty[month] = total_monthly_licenced_qtys[month] + total_approval_monthly_licenced_qtys[month]
            total_return[month] = total_monthly_return_qtys[month] + total_approval_monthly_return_qtys[month]
            total_absolute[month] = total_monthly_absolute_qtys[month] + total_approval_monthly_absolute_qtys[month]

        print(total_qty, total_return, total_absolute)

compute_station_quantities()

# for zone, rows in df.groupby('hydrological_zone'):
#     rows.to_csv(f'../data/4_training/{output_directory}/{round(zone)}.csv', index=False, header=True)
