export const WatershedModelDescriptions = {
  drainageArea: {
    name: 'Drainage Area',
    description: 'Total area of the selected watershed measured in kilometers squared (km^2).',
    url: ''
  },
  annualPrecipitation: {
    name: 'Annual Precipitation',
    description: 'Total annual rainfall over the selected watershed area measured in milimeters (mm). ' +
    'This is received from the Pacific Climate organization precipitation api ' +
    '(https://services.pacificclimate.org/pcex/api/timeseries)',
    url: 'https://pacificclimate.org/'
  },
  glacialCoverage: {
    name: 'Glacial Coverage',
    description: 'Percentage glacial coverage over the selected watershed area. This is calculated ' +
    'by taking the selected watershed polygon and performing an intersect against the DataBC layer ' +
    'Freshwater Atlas Glaciers.',
    url: 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-glaciers'
  },
  medianElevation: {
    name: 'Median Elevation',
    description: 'Median elevation is ideal but the dataset we have access to currently only support mean elevation over the watershed area. ' +
    'The data is sourced from https://apps.gov.bc.ca/gov/sea/slopeElevationAspect/json which is an api that returns a SlopeElevationAspectResult ' +
    'containing the following variables: ' +
    'slope: The slope of the best fit plane based on elevation points found within or around the input geometry. ' +
    'A slope may be returned as NULL in the case where there was insufficient data available to calculate the value. Slope is returned as a percentage from 0 to 100 (100% = straight up, 50% = 45 degree slope). ' +
    'minElevation: The minimum elevation of a point found within or around the input geometry. ' +
    'maxElevation: The maximum elevation of a point found within or around the input geometry. ' +
    'averageElevation: The minimum elevation of a point found within or around the input geometry. ' +
    'aspect: Aspect is a measure of the orientation or exposure of an area by means of compass points (e.g. 180 degrees - south). Permitted values 0 – 359. An aspect may be returned as NULL in the case where there was insufficient data available to calculate the value. ' +
    'confidenceIndicator: A value based on the accumulated error between the plane and each of the DEM points. The lower the value the better where 0 represents a perfect fit. The larger the feature the higher probability of a low confidence value.',
    url: 'http://apps.gov.bc.ca/gov/sea/index.html'
  },
  meanAnnualDischarge: {
    name: 'Mean Annual Discharge',
    description: 'This value is calculated from the output of the Mean Annual Runoff (MAR) multivariate model. ' +
    'To calculate Mean Annual Discharge the following equation is used: MAD = MAR / 1000 * DRAINAGE_AREA.' +
    'MAR is an output of a multivariate model sourced from a scientific hydrological paper. ' +
    'The model has trained co-efficients for three hydrological zones (25, 26, 27) from the DataBC hosted layer: Hydrology: Hydrologic Zone Boundaries of British Columbia: ' +
    'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrologic-zone-boundaries-of-british-columbia ' +
    'The inputs used in calculting MAR are as follows: <br>' +
    '  drainage area, glacial coverage, median elevation, annual precipitation, evapo-transpiration, solar exposure, and average slope. ' +
    '  These inputs are multiplied by trained co-efficient values and adjusted by an intercept to output a predicted MAR value in l/km^2/s. ' +
    '  The source paper is linked below.',
    url: ''
  },
  meanAnnualRunoff: {
    name: 'Mean Annual Runoff',
    description: 'MAR is an output of a multivariate model sourced from a scientific hydrological paper. ' +
    'The model has trained co-efficients for three hydrological zones (25, 26, 27) from the DataBC hosted layer: Hydrology: Hydrologic Zone Boundaries of British Columbia: ' +
    'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrologic-zone-boundaries-of-british-columbia ' +
    'The inputs used in calculting MAR are as follows: <br>' +
    '  drainage area, glacial coverage, median elevation, annual precipitation, evapo-transpiration, solar exposure, and average slope. ' +
    '  These inputs are multiplied by trained co-efficient values and adjusted by an intercept to output a predicted MAR value in l/km^2/s. ' +
    '  The source paper is linked below.',
    url: ''
  },
  low7Q2: {
    name: 'Low7Q2',
    description: '2-year annual 7-day low flow.',
    url: ''
  },
  dry7Q10: {
    name: 'Dry7Q10',
    description: '10-year dry return period 7-day late summer (Jun-Sep) low flow.',
    url: ''
  },
  monthlyDischarge: {
    name: 'Monthly Discharge',
    description: 'This section displays a table and chart of the mean monthly discharges, volume discharge, and percentage of mean annual discharge.',
    url: ''
  },
  monthlyDistribution: {
    name: 'Monthly Distribution',
    description: '',
    url: ''
  },
  availabilityVsDemand: {
    name: 'Availability vs Licenced Quantity',
    description: 'This section shows all the water rights licences found within the watershed, and compares the licenced quantity against the calculated availability.',
    url: ''
  }
}
