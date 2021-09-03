# Computing hydrostats

## Prerequisites

* R
* Python
* fasstr (https://bcgov.github.io/fasstr/)

## Bulk computing from a csv file

`bulk_calculate_quantiles.py` will take a `watershed_stats.csv` file (with station numbers in the first column), and add 7Q2, 7Q10, 30Q5 and 30Q10 columns
for each station.
The output file is hardcoded to `stats_quantiles_out.csv`.  Again, if re-using this script, go ahead and add in-file and out-file parameters.  Refactoring
everything to R is probably a better solution than wrapping the scripts with Python.

## Get a list of stations

```sh
curl 'https://openmaps.gov.bc.ca/geo/pub/wfs?service=WFS&request=GetFeature&count=10000&srsName=EPSG%3A3005&version=2.0&outputFormat=csv&typeName=WHSE_ENVIRONMENTAL_MONITORING.ENVCAN_HYDROMETRIC_STN_SP' | cut -d , -f3 > watershed_stats.csv
```

## Computing a single low flow

```sh
Rscript compute_quantile.r <station_name> <roll_days> <return_period>
```

To use FASSTR directly from within R studio, refer to the fasstr docs linked above.

## Summer low flows (Jun-Sept)

```sh
Rscript compute_quantile_summer.r <station_name> <roll_days> <return_period>
```

`compute_quantile_summer.r` is just the `compute_quantile.r` script copied and modified to add `months=6:9`.  In the future, if this script gets reused, refactoring this
into one R script might be helpful.


curl 'https://openmaps.gov.bc.ca/geo/pub/wfs?service=WFS&request=GetFeature&count=10000&srsName=EPSG%3A3005&version=2.0&outputFormat=csv&typeName=WHSE_ENVIRONMENTAL_MONITORING.ENVCAN_HYDROMETRIC_STN_SP' 