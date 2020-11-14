import requests
import json
from pprint import pprint
import urllib3
import math as m
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set up connection parameters in a dictionary
gateway = {"ip": "CONTROLLER_IP", "port": "8443"}

# set REST API headers
headers = {"Accept": "application/json",
        "Content-Type": "application/json"}
# set URL parameters
loginUrl = 'api/login'
url = f"https://{gateway['ip']}:{gateway['port']}/{loginUrl}"
# set username and password
body = {
    "username": "USERNAME",
    "password": "PASSWORD"
}
# Open a session for capturing cookies
session = requests.Session()
# login
response = session.post(url, headers=headers,
                        data=json.dumps(body), verify=False)

# parse response data into a Python object
api_data = response.json()
print("/" * 50)
pprint(api_data)
print('Logged in!')
print("/" * 50)

# Set up to get site name
getSitesUrl = 'api/self/sites'
url = f"https://{gateway['ip']}:{gateway['port']}/{getSitesUrl}"
response = session.get(url, headers=headers,
                    verify=False)
api_data = response.json()
# Parse out the resulting list of
responseList = api_data['data']
n = 'name'
for items in responseList:
    if items.get('desc') == 'SITE_NAME':
        n = items.get('name')
print(n)

getDevicesUrl = f"api/s/{n}/stat/sta"
url = f"https://{gateway['ip']}:{gateway['port']}/{getDevicesUrl}"
response = session.get(url, headers=headers,
                    verify=False)
api_data = response.json()
responseList = api_data['data']
print('DEVICE LIST AND STATUS')
for device in responseList:

    if device['ap_mac'] != "" & device['ap_mac'] == "ACCESS_POINT_MAC_ADD":
        print(f"Signal = {device['signal']}")
        print(f"AP MAC = {device['ap_mac']}")
        distance = m.pow(10.0, ((27.55) - (20 * m.log10(5200)) + abs(device['signal'])) / 20.0)
        print(abs(distance), "M")