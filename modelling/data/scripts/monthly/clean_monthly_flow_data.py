import json
import datetime

with open('../../output/db/dlyflows_gt2000_fullmonth.json') as flow_file:
    flow_data = json.load(flow_file)

print("pre-count: {}".format(len(flow_data)))

reduced_flow_data = []

# remove flow data with year below 2000
for i in range(len(flow_data)):
    if flow_data[i]["YEAR"] >= 2000:
        reduced_flow_data.append(flow_data[i])

print("post-count: {}".format(len(reduced_flow_data)))

date = datetime.datetime.now().strftime('%m-%d-%Y')
filename = "station_flow_values" + "_" + date + ".json"

# write stations information to file
with open("../../output/flow/" + filename, "w") as outfile:
    json.dump(reduced_flow_data, outfile)