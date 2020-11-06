# Water Modelling

### Purpose

This folder contains scripts for extracting HYDAT water data and pytorch based modelling tools to analyze and estimate the predictive value of water flow data.

### Running the scripts

Suggested method to run these scripts is to create a new venv and install the requirements.txt file using pip. 
Then you can run any script by simply running it as python.

### Data

In the data folder file sql_queries.sql you will find some useful mysql queries that extract table information form the HYDAT mysql database. The most recent version of HYDAT can be 
accessed here: [HYDAT Download Page](https://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/)
The version used on the intial training won't be included in the repo due to the apprx 2GB size so you will need to download the HYDAT.sqlite3 from the above link first.

Under the scripts directory you will find some python scripts that merge together the extracted HYDAT data with information from WALLY's backend. The main purpose of this step is to merge the station information with the relevant water modelling inputs such as annual_precipitation, drainage_area etc. The surface water tool api is used to gather this information.
There are two steps to getting the data from wally.

1. Use the station LATITUDE/LONGITUDE point to call the watershed endpoint and get the cached watershed ID. 
2. With this id we then query the surface water analysis endpoint which gives us the relevant input variables

Once you have the data from wally, you need to merge it with the station information using the scripts in the data folder. This data is then used as the training data set for use in the modelling scripts.

Some generated datasets have been left in the output folder as an example, but flow data and the training data sets are not included in the repo due to size. This means it needs to be generated locally before modelling can occur. With more effort this process can be automated but currently requires manual running of the download and merging scripts.

### Modelling

Under the models directory there are annual and monthly modelling scripts that are primarily made up of pytorch modules. 
The annual model attempts to predict mean annual discharge by using a small 2 layer neural network. This should be scaled up with better hardware for training.


### Minio Model State Storage

The wally api backend pulls model state information from the cluster minio instance. This data is stored in the models bucket and structured using the follwing directories:

    /models/v1/hydro_zone_annual_flow/
    /models/v2/hydro_zone_annual_flow/
    /models/v2/hydro_zone_monthly_distributions/

The following commands are examples on how to upload the data from the wally/modelling/v2/model_output project directory:

    mc cp --recursive hydro_zone_annual_flow/ wally-dev/models/v2/hydro_zone_annual_flow/
    mc cp --recursive hydro_zone_monthly_distributions/ wally-dev/models/v2/hydro_zone_monthly_distributions/
  