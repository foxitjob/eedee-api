import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hlcms.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from api.models import Wechat_site
from django.utils import timezone
from api.util.weixin import WechatClient
from api.util.logger_helper import init_logger
import time


def refreshToken():
    logger = init_logger("refreshToken")
    wechatsites = Wechat_site.objects.all()
    for site in wechatsites:
        if site.accesstoken:
            print "localtime = ", timezone.now()
            print "tokenTime =", site.gettokentime
            print (timezone.now() - site.gettokentime).seconds
            print time.mktime(timezone.now().timetuple())
            print time.mktime(site.gettokentime.timetuple())
            if (time.mktime(timezone.now().timetuple()) - time.mktime(
                    site.gettokentime.timetuple())) > site.expires_in - 3600:
                logger.info("will request new accesstoken")
                wechatclient = WechatClient(site.appid, site.appsecret)
                result = wechatclient.get_accesstoken()
                if result['access_token']:
                    __createAccessToken(site, result)
        else:
            print "token is not exist, will create it now"
            wechatclient = WechatClient(site.appid, site.appsecret)
            result = wechatclient.get_accesstoken()
            if result['access_token']:
                __createAccessToken(site, result)


def __createAccessToken(site, content):
    site.accesstoken = content['access_token']
    site.expires_in = content['expires_in']
    site.gettokentime = timezone.now()
    # print "the new access token is: %s, will save it now"% site.accesstoken
    site.save()


def getToken(appid=None):
    wechatsite = Wechat_site.objects.get(appid=appid)
    accesstoken = wechatsite.accesstoken
    return accesstoken


if __name__ == '__main__':
    refreshToken()
    appid = 'wx4c40f5900aa7efd0'
    appsecret = 'eede69ee1c02a23f011f22f94f8d3905'
    accesstoken = getToken(appid)
    WechatClient(appid, appsecret).create_menu(accesstoken)
