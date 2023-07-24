# WALLY Modelling Guide

Here's a guide to get started with the WALLY modelling code

The main steps involved are as follows:

1. Download HYDAT sqlite database
2. Use sql queries in the /sql folder to get station flow values for stations in BC
3. Flatten station yearly flow values into one data row by running flatten_mean_annual_flows.py script
4. Upload flattened data to WALLY Minio instance under /modelling bucket
5. Run WALLY Openshift Watershed characteristics/licence information job (long-running)
6. Create Allocation and Return coefficients for all Purpose types in dataset
7. Build training dataset by running building_latest_training_data.py script 
8. Run modelling script by configuring and running the input_variation_hydro_zone_model.py script
9. Analyze outputted reports in the /models/output folder for results

## Step 1 - Download HYDAT sqlite DB

Download the latest HYDAT data from the following endpoint
https://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/
filename looks like this if you substitue a date: Hydat_sqlite3_<date>.zip

## Step 2 - Query HYDAT DB

Under the /sql folder there is a sql_queries.sql file that contains various useful queries.
The one to generate flow values is under the comment 'MAIN SOURCE DATA QUERY'
Using a sqlite program with the HYDAT db attached, run the main source data query 
to generate the resulting flow values. This data should be saved as a csv file.

## Step 3 - Flatten Flow Data

The HYDAT source data has data for all years that a station was active. We only need an average of all years,
so we need to 'flatten' the data to only include one data row per station.

To do this run the flatten_mean_annual_flows.py script under /scripts against the outputted csv file from the previous step. This will give you a flattened csv of flow values, one for each station.

## Step 4 - Upload source data to Minio

The next step requires access to the WALLY Minio storage system. This is located in the WALLY Openshift environment. There is a s3 bucket called 'modelling' which we need to upload the flattened data to in order
to run the next step in the process. 
* The filename should be called 'bc_mean_annual_flows_flattened.csv' 
There is a job that looks for this file in the /modelling minio bucket

## Step 5 - Run the watersehd-stats-job in Openshift

Next we need to run the job in Openshift that queries the WALLY API for watershed and licensing information.
This job performs the following:
1. Delineates a watershed boundary based upon the station location
2. Generates watershed characteristics such as annual_precipitation, glacial_coverage, area etc.
3. Aggregates together all water licences (long and short term) that are found within the watershed boundary

from the /oc_job directory run the following openshift command after logging in through terminal:
oc process -p MINIO_HOST_URL=wally-minio-staging:9000 -f scrape_watershed_data.job.yaml | oc -n d1b5d2-test apply -f -

if the watershed-stats-job already exists you may have to delete the existing job with the following command:
oc delete job watershed-stats-job

This is a long-running task and can take up to 36 hours to generate data for all stations in BC
The job will generate 3 files and upload them to the Minio /modelling bucket as output:
1. Watershed Characteristics - watershed_stats_output_<date>.csv
2. Watershed Licence Info - watershed_licence_output_<date>.csv
3. Watershed Approvale Info (short term licences) - watershed_approvals_output_<date>.csv

Download these resulting scraped files from Minio /modelling bucket and store them on your local computer for later use.

## Step 6 - Create Allocation/Return value Coefficients for all purpose types in dataset

As part of building monthly licensing use values we need a list of licence purpose type allocation and return values. This was provided by subject matter expert, and these values can change over time so updating them 
annually is suggested.

The files should be csv files with at least the following columns:
Allocation:
Purpose_Num,Units,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,Sum
Return:
Purpose_Num,Units,Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec,Sum

## Step 7 - Build Training Data

- The training data is built from a combination of the following data sources
1. HYDAT sqlite database
2. WALLY Licensing information API
3. Monthly Allocation values (Manual creation)
4. Monthly Return values (Manual creation)

There is a file in the /scripts directory call build_latest_training_data.py which will take all of the data gathered so far
and output the training data files. The output directory can be configured within the script. 

This script will generate training data for each hydrological zone in BC numbered 1.csv - 29.csv. It also outputs a file called
all_data.csv which contains all data aggregated together. These files can be used in the following steps to build different model outputs.

## Step 8 - Run Modelling Scripts

In order to run the modelling scripts, you will need the following python environment setup on your local machine

- Pre-requisites:
* you will need python 3 installed on your machine
* Use the following terminal command from the root of this project to get the right packages installed

- Terminal commands for project setup
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt 

At this point you should have all of the training data ready and python environment setup to start running models. 

A multi-variate linear model that can be used is the input_variation_hydro_zone_model.py file that resides in the /model folder
This model auto-matically tries every combination of input parameters to find the most robust input set based upon highest minimum R2 values.
The 'winning' input set is then re-trained using all training data in order to output the best possible performant model.
This script in-particular will generate reports for every fold that is tested, along with a summary report that displays all folds together.
The output will be located in the models/output/ directory

## Step 9 - Review and Analyze Output

Many models can be built and tested against the created training data. Analysis of each model is up to the creators intuition but generally
measurements of R2 and RMSE for the multi-variate linear model are the best measures of model accuracy. 
