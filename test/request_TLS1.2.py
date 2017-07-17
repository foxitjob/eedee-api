import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_2,
                                       # ssl_version=ssl.PROTOCOL_TLSv1_2
                                       )

def prn_obj(obj):
    print ', '.join(['%s:%s' % item for item in obj.__dict__.items()])


s = requests.Session()

s.mount('https://', MyAdapter())
r = s.get('https://www.baidu.com', verify=False)
print r.text

import base64

base64string = base64.encodestring(
    '%s:%s' % ("sodadmin", "Start123!"))[:-1]
authheader = "Basic %s" % base64string

headers = {'authorization': authheader,
           'content-type': 'application/json'}
requests.packages.urllib3.disable_warnings()

r = s.get('https://16.157.134.154:8136/sod_lvm/', headers=headers, verify=False)
print r.text
print r.status_code
