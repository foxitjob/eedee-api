from api.services.tokenservice import *
from django.test import TestCase

class refreshTokenTestCase1(TestCase):
    def setUp(self):
        name='gh_fdf7baf446ae'
        appid='wx4c40f5900aa7efd0'
        appsecret='eede69ee1c02a23f011f22f94f8d3905'
        Wechat_site.objects.create(name=name, appid=appid, appsecret=appsecret)

    def tearDown(self):
        pass

    def testrefreshToken(self):
        refreshToken()
        self.assertIsNotNone(Wechat_site.objects.get(name='gh_fdf7baf446ae').accesstoken)
        self.assertIsNotNone(Wechat_site.objects.get(name='gh_fdf7baf446ae').gettokentime)


