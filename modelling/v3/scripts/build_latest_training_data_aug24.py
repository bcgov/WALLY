from datetime import datetime
from numpy.core.records import record
import pandas as pd
import csv
import json
import ast

# station_number,most_recent_year,years_of_data,mean,min,max,drainage_area_gross,latitude,longitude,gen_id,annual_precipitation,aspect,average_slope,drainage_area,glacial_area,glacial_coverage,hydrological_zone,median_elevation,potential_evapotranspiration,solar_exposure,watershed_area
df = pd.read_csv("../data/2_scrape_results/july30_licence_data/watershed_stats_output.csv")

# PRE-FILTER STATION DATA

# 20 percent discrepancy
indexNames = df[((df['drainage_area'] / df['drainage_area_gross']) - 1).abs() <= 0.2].index
df = df.iloc[indexNames]

# years of data
df = df[df["years_of_data"] > 10]

# ignore certain stations
# df = df[df["station_number"] != "08MH002"]
# df = df[df["station_number"] != "08MH005"]

# Mar adjustment
# df['mean'] = (df['mean'] / df['drainage_area']) * 1000
# add MAR as separate column ************
df['mar'] = (df['mean'] / df['drainage_area']) * 1000


# IMPORT LICENCE DATA
# station_number, gen_id, approvals, total_qty, projected_geometry_area, projected_geometry_area_simplified
df_approvals = pd.read_csv("../data/2_scrape_results/july30_licence_data/watershed_approvals_output.csv")
# station_number, gen_id, licences, inactive_licencese, total_qty, total_qty_by_purpose, projected_geometry_area, projected_geometry_area_simplified
df_licences = pd.read_csv("../data/2_scrape_results/july30_licence_data/watershed_licence_output.csv")

# IMPORT ALLOCATION VALUES
# Purpose_Num, Consumptive?, Purpose, Units, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Sum, PREVIOUS_monthly_coefficients, Description of Water License Purpose, Reference/Note
df_allocation_coef = pd.read_csv("../data/2_scrape_results/july30_licence_data/monthly_allocation_coefficients.csv")
# Purpose_Num, Consumptive?, Purpose, Units, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec, Sum, Reference
df_return_coef = pd.read_csv("../data/2_scrape_results/july30_licence_data/monthly_return_coefficients.csv")
# PURPOSE_USE_CODE == Purpose_Num

monthly_licenced_output = []# pd.DataFrame([], columns=['station_number', 'monthly_licenced_qty', 'monthly_licenced_return', 'monthly_licenced_absolute'])

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
    for index, station in df.iterrows():
        station_number = station['station_number']
        licence_records = df_licences.loc[df_licences['station_number'] == station_number]
        approval_records = df_approvals.loc[df_approvals['station_number'] == station_number]
        
        oldest_priority_date = datetime.now()

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

                # find oldest licence priority date 1999-01-25Z
                priority_date = properties['PRIORITY_DATE'].replace('Z', '')
                priority_date = datetime.strptime(priority_date, '%Y-%m-%d')
                if oldest_priority_date > priority_date:
                    oldest_priority_date = priority_date

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

        monthly_licenced_qty = {}
        monthly_licenced_return = {}
        monthly_licenced_difference = {}
        for month in MONTHS:
            monthly_licenced_qty['qty_' + month] = total_monthly_licenced_qtys[month] + total_approval_monthly_licenced_qtys[month]
            monthly_licenced_return['return_' + month] = total_monthly_return_qtys[month] + total_approval_monthly_return_qtys[month]
            monthly_licenced_difference['abs_' + month] = total_monthly_absolute_qtys[month] + total_approval_monthly_absolute_qtys[month]

        annual_licenced_qty = sum(c for c in monthly_licenced_qty.values())
        annual_licenced_return = sum(c for c in monthly_licenced_return.values())
        annual_licenced_abs = sum(c for c in monthly_licenced_difference.values())
        
        # print(monthly_licenced_qty, monthly_licenced_return, monthly_licenced_difference)
        monthly_licenced_output.append({
          'station_number': station_number,
          **monthly_licenced_qty, 
          **monthly_licenced_return, 
          **monthly_licenced_difference,
          'annual_qty': annual_licenced_qty,
          'annual_return': annual_licenced_return,
          'annual_abs': annual_licenced_abs,
          'percent_allocated_mad': (annual_licenced_qty / 31536000) / station['mean'],
          'percent_allocated_mad_abs': (annual_licenced_abs / 31536000) / station['mean'],
          'oldest_priority_date': oldest_priority_date.strftime("%d/%m/%Y")
        })

compute_station_quantities()


# ***** EXPORT *****
print(df)
print(monthly_licenced_output)

df_monthlys = pd.DataFrame(monthly_licenced_output, columns=monthly_licenced_output[0].keys())
# merge watershed stats with monthly licence outputs
df_merged = pd.merge(df, df_monthlys, on='station_number')

# export to files
output_directory = "aug24"

# output by all_data
df_merged.to_csv(f'../data/4_training/{output_directory}/all_data.csv', index=False, header=True)

# output by zone
for zone, rows in df_merged.groupby('hydrological_zone'):
    rows.to_csv(f'../data/4_training/{output_directory}/{round(zone)}.csv', index=False, header=True)
