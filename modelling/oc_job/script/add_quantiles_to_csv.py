"""
script to augment a file "watershed_stats.csv" with quantiles computed using FASSTR.
The output CSV with the flow quantiles (7Q10, 7Q2, 30Q10, 30Q5) will be "./stats_quantiles_out.csv".
see `compute_quantile.r` for the R script that calls the FASSTR functions.
This is mean to be a one off script until the FASSTR functions can be integrated with
scrape_stations.py.
"""

import asyncio
import subprocess
import csv


async def compute(stn, days, return_period) -> str:
    proc = await asyncio.create_subprocess_shell(
        " ".join(['Rscript', './compute_quantile.r', stn, days, return_period]),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    result = ""

    stdout, stderr = await proc.communicate()
    if proc.returncode == 0:
        result = stdout.decode().strip().split('\n')[-1:][0]

    if stdout:
        print(f'[{stn}] calculated {days}q{return_period}: {result}')
    if stderr:
        print(f'[{stn}] skipping {days}q{return_period}: {stderr.decode()}')

    return result


async def add_7q10(in_filename: str, out_filename: str):
    """ add 7q10 column to a csv of streamflow data """

    with open(in_filename, 'r', newline='') as in_file, open(out_filename, 'a', newline='') as out_file:
        flow_reader = csv.reader(in_file)
        flow_writer = csv.writer(out_file)

        headers = next(flow_reader)
        headers = headers + ["7Q10", "7Q2", "30Q5", "30Q10"]
        flow_writer.writerow(headers)

        for row in flow_reader:
            stn = row[0]
            low_7q10 = compute(stn, "7", "10")
            low_7q2 = compute(stn, "7", "2")
            low_30q5 = compute(stn, "30", "5")
            low_30q10 = compute(stn, "30", "10")


            values = await asyncio.gather(low_7q10, low_7q2, low_30q5, low_30q10)
            new_row = row + values
            flow_writer.writerow(new_row)


if __name__ == "__main__":
    asyncio.run(add_7q10("./watershed_stats.csv", "./stats_quantiles_out.csv"))
