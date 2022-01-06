#!/usr/bin/python
import json
import requests
import sys
from collections import namedtuple

TEST_AGENT_URL = "https://test-agent.foodtruck-staging.com"
FLEET_INV_URL = "https://fleetinv.foodtruck-qa.com"


def TruckSession(object):
    return namedtuple('X', object.keys())(*object.values())


#     def __init__(self,truck_session_ids):
#         self.truck_session_ids = truck_session_ids

def jsonToObject(d):
    # convert dict to object
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items())  # get args
        inst = class_(**args)  # create new instance
    else:
        inst = d
    return inst


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# get picking list restaurant
response = requests.get("%s/truck-session/bulk-create-input" % TEST_AGENT_URL)
if response.status_code == 200:
    print("get picking list restaurant succeed.")
else:
    print("get picking list restaurant failed.")
    print("fail response: %s" % response.status_code)
    sys.exit()
jprint(response.json())
restaurant = response.json()
# print(restaurant)
# print(response.text)
# print(json.dumps(restaurant))


# create truck session
inputs = restaurant
headers = {'Content-type': 'application/json'}
response = requests.post("%s/truck-session/bulk-create" % TEST_AGENT_URL, headers=headers, json=restaurant)
if response.status_code == 201:
    print("create truck session succeed.")
else:
    print("create truck session failed.")
    print("fail response: %s" % response.status_code)
    sys.exit()

# truckSession = json.loads(jsonToObject(response.text), object_hook=TruckSession)
truckSession = response.json()
print("create truck session response:\n")
jprint(response.json())

# get picking list template
# inputs = {
#             "truck_session_ids": [
#                 26735
#             ]
#         }
inputs = truckSession.truck_session_ids
headers = {'Content-type': 'application/json'}
response = requests.put("%s/excel/truck-session/download-picking-list" % TEST_AGENT_URL, headers = headers, json =truckSession)
if response.status_code == 200:
    print("get picking list template succeed.")
else:
    print("get picking list template failed.")
    print("fail response: %s" % response.status_code)
    sys.exit()
with open("./Picking List Template.xlsx", 'wb') as file:
    file.write(response.content)

# upload picking list (disable)
files = {'file': open('./Picking List Template.xlsx', 'rb')}
response = requests.post("%s/truck-logistic-site/excel/truck-session/bulk-upload-picking-list" % FLEET_INV_URL,
                         files=files)
if response.status_code == 200:
    print("upload picking list succeed.")
else:
    print("upload picking list failed.")
    print("fail response: %s" % response.status_code)
    sys.exit()
jprint(response.json())

# check picking list
files = {'file': open('./Picking List Template.xlsx', 'rb')}
response = requests.post(
    "%s/truck-logistic-site/excel/truck-session/check-bulk-upload-picking-list-data" % FLEET_INV_URL, files=files)
if response.status_code == 200:
    print("check picking list succeed.")
else:
    print("check picking list failed.")
    print("fail response: %s" % response.status_code)
    sys.exit()
jprint(response.json())
