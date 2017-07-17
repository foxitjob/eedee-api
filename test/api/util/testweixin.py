from api.util.weixin import *
import unittest

class WexinTestCase1(unittest.TestCase):
    def setUp(self):
        appid = "wx4c40f5900aa7efd0"
        appsecret = "eede69ee1c02a23f011f22f94f8d3905"
        self.client = WechatClient(appid, appsecret)

    def tearDown(self):
        pass

    def testget_accesstoken(self):
        self.client.get_accesstoken()

