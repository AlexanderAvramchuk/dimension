from django.test import TestCase
import requests

data = {
    "name": "testName",
    "registration_id": "f9aea05acb5ef24f2dcc8559c75e1ba544c3c5523e98e1874561233ef0a9c17a",
    "device_id": "949b4b39-cdff-4f36-a1bd-2177fcf81770",
    "active": True
}
register_apns_url = "http://5.101.116.20:8885/api/register_apns/"


r = requests.post(register_apns_url, data=data)
print str(r.status_code)