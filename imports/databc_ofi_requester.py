import requests
import json
import pprint


def send_request():
    url = "https://apps.gov.bc.ca/pub/dwds-ofi/"
    path = "order/createOrderFiltered" # createOrderFilteredSM

    with open('geojson_request.json', 'r') as f:
        layers_dict = json.load(f)

    layers_dict['emailAddress'] = 'daine.trinidad@gov.bc.ca'
    # pprint.pprint(layers_dict)
    # print("requesting", url+path)
    # input_json_obj = {
    #     "emailAddress": "daine.trinidad@gov.bc.ca",
    #     "aoiType": "8",
    #     "aoi": "",
    #     "crsType": "0",
    #     "clippingMethodType": "0",
    #     "formatType": "6",
    #     "useAOIBounds": "0",
    #     "aoiName": "092B061,092C070",
    #     "prepackagedItems": "",
    #     "orderingApplication": "DWDS-OFI-Tester",
    #     "featureItems": [
    #         {
    #             "featureItem": "WHSE_ADMIN_BOUNDARIES.CLAB_INDIAN_RESERVES", "filterValue": "objectid > 0"
    #         },
    #         {
    #             "featureItem": "WHSE_ADMIN_BOUNDARIES.CLAB_NATIONAL_PARKS",
    #             "filterValue": "ENGLISH_NAME like '%UNNAMED%'"
    #         }
    #     ]
    # }

    payload = {
        # "inputJsonObj": input_json_obj
        "inputJsonObj": layers_dict
    }

    headers = {"Content-type": "application/json"}
    pprint.pprint(payload)
    # response = requests.post(url + path, payload)
    response = requests.post(url+path, data=json.dumps(payload), headers=headers)
    pprint.pprint(response.status_code)
    pprint.pprint(response.text)
    # data = response.json()
    # pprint.pprint(data)

    orderID = response.text

send_request()
