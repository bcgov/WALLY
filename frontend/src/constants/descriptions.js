export const WatershedModelDescriptions = {
  drainageArea: {
    name: 'Drainage Area',
    description: 'Total area of the selected watershed measured in kilometers squared (km²).',
    url: ''
  },
  annualPrecipitation: {
    name: 'Annual Precipitation',
    description: 'Total annual rainfall over the selected watershed area measured in millimeters (mm). ' +
    'Hamann, A. and Wang, T., Spittlehouse, D.L., and Murdock, T.Q. 2013. A comprehensive, high-resolution ' +
    'database of historical and projected climate surfaces for western North America. Bulletin of the ' +
    'American Meteorological Society 94: 1307–1309.' +
    'https://sites.ualberta.ca/~ahamann/data/climatewna.html',
    url: 'https://sites.ualberta.ca/~ahamann/data/climatewna.html'
  },
  glacialCoverage: {
    name: 'Glacial Coverage',
    description: 'Percentage glacial coverage over the selected watershed area, ' +
    'using data from Freshwater Atlas Glaciers.',
    url: 'https://catalogue.data.gov.bc.ca/dataset/freshwater-atlas-glaciers'
  },
  medianElevation: {
    name: 'Mean elevation',
    description: 'Mean elevation for the watershed area from the FLNRORD Slope Elevation Aspect service ' +
    'http://apps.gov.bc.ca/gov/sea/index.html (accessible from internal Province of British Columbia networks)',
    url: 'http://apps.gov.bc.ca/gov/sea/index.html'
  },
  meanAnnualDischarge: {
    name: 'Mean Annual Discharge',
    description: 'This value is calculated from the output of the Mean Annual Runoff (MAR) multivariate model. ' +
    'To calculate Mean Annual Discharge the following equation is used: MAD = MAR / 1000 * DRAINAGE_AREA. ' +
    'MAR is an output of a multivariate model sourced from a scientific hydrological paper. ' +
    'The model has trained co-efficients for three hydrological zones (25, 26, 27) from the DataBC hosted layer: ' +
    'Hydrology: Hydrologic Zone Boundaries of British Columbia: ' +
    'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrologic-zone-boundaries-of-british-columbia ' +
    'The inputs used in calculting MAR are as follows: <br>' +
    '  drainage area, glacial coverage, median elevation, annual precipitation, evapo-transpiration, solar exposure, ' +
    'and average slope. These inputs are multiplied by trained co-efficient values and adjusted by an intercept to ' +
    'output a predicted MAR value in l/km²/s. The source paper is linked below.',
    url: ''
  },
  potentialEvapotranspiration: {
    name: 'Potential Evapotranspiration',
    description: 'Trabucco, Antonio; Zomer, Robert (2019): Global Aridity Index and Potential' +
    'Evapotranspiration (ET0) Climate Database v2. figshare. Dataset. https://doi.org/10.6084/m9.figshare.7504448.v3',
    url: 'https://cgiarcsi.community/data/global-aridity-and-pet-database/'
  },
  meanAnnualRunoff: {
    name: 'Mean Annual Runoff',
    description: 'MAR is an output of a multivariate model sourced from a scientific hydrological paper. ' +
    'The model has trained co-efficients for three hydrological zones (25, 26, 27) from the DataBC hosted ' +
    'layer: Hydrology: Hydrologic Zone Boundaries of British Columbia: ' +
    'https://catalogue.data.gov.bc.ca/dataset/hydrology-hydrologic-zone-boundaries-of-british-columbia ' +
    'The inputs used in calculting MAR are as follows: <br>' +
    ' drainage area, glacial coverage, median elevation, annual precipitation, evapo-transpiration, solar ' +
    'exposure, and average slope. These inputs are multiplied by trained co-efficient values and adjusted ' +
    'by an intercept to output a predicted MAR value in l/km²/s. The source paper is linked below.',
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
    description: 'This section displays a table and chart of the mean monthly discharges, volume discharge, ' +
    'and percentage of mean annual discharge. These values are produced as ouput from the above model.',
    url: ''
  },
  monthlyDistribution: {
    name: 'Monthly Distribution',
    description: '',
    url: ''
  },
  waterRightsLicenceDemand: {
    name: 'Water Rights Licences',
    description: 'This section shows all the water rights licences found within the watershed. Water rights ' +
    'licences are sourced from the DataBC layer "Water Rights Licences - Public" linked below. Licences ' +
    'associated with a groundwater point of diversion have not been included as part of this calculation.',
    url: 'https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public'
  },
  availabilityVsDemand: {
    name: 'Availability vs Licenced Quantity',
    description: 'This section shows all the water rights licences found within the watershed, ' +
    'and compares the licenced quantity against the calculated availability. Water rights licences are ' +
    'sourced from the DataBC layer "Water Rights Licences - Public" linked below.',
    url: 'https://catalogue.data.gov.bc.ca/dataset/water-rights-licences-public'
  },
  totalAnnualQuantity: {
    name: 'Total Annual Quantity',
    description: 'This section shows the total amount of water drained by this watershed ' +
    ' per year in cubic metres (m³).',
    url: ''
  },
  shortTermDemand: {
    name: 'Water Approval Points (Short Term Licences)',
    description: 'This section shows all the water approval points found within the watershed. ' +
    'Water approval points are sourced from the DataBC layer "Water Approval Points" linked below.',
    url: 'https://catalogue.data.gov.bc.ca/dataset/water-approval-points'
  }
}
