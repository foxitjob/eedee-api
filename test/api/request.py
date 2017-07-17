import requests
from requests.auth import HTTPBasicAuth

# GET:
r = requests.get('https://api.github.com', )
print r.status_code
print r.text
print r.encoding

# POST:
# payload = {'key1': 'value1', 'key2': 'value2'}
# r = requests.post('https://api.github.com', data=payload)
# print r.text
# auth
from requests.auth import HTTPDigestAuth

import base64

base64string = base64.encodestring(
    '%s:%s' % ("sodadmin", "Start123!"))[:-1]
authheader = "Basic %s" % base64string

headers = {'authorization': authheader,
           'content-type': 'application/json'}
requests.packages.urllib3.disable_warnings()
r = requests.get('https://16.157.134.154:8136/sod_lvm/', headers=headers, verify=False)
print r.text
print r.status_code