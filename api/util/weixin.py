#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from api.util.logger_helper import init_logger
from message import *
from api.models import Wechat_site
import urllib


class WechatClient():
    def __init__(self, appid, appsecret):
        self.APPID = appid
        self.APPSECRET = appsecret

    def get_accesstoken(self):
        logger = init_logger('get_accesstoken')
        logger.debug("Begin request the accesstoken")
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.APPID,
                                                                                                           self.APPSECRET)
        response = requests.request("GET", url, verify=True)

        if response.status_code == 200:
            result = json.loads(response.content)
            return result
        else:
            # throw exception
            pass


    def get_accesstoken_from_db(self):
        logger = init_logger('get_accesstoken_from_db')
        logger.debug("Begin request the accesstoken from db")
        wechat_site = Wechat_site.objects.get(appid=self.APPID)
        return wechat_site.accesstoken

    def create_menu(self, accesstoken):
        logger = init_logger('create_menu')
        menu = {
            "button": [
                {
                    "type": "click",
                    "name": "按钮2",
                    "key": "V1001_TODAY_MUSIC"
                },
                {
                    "name": "menu",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "搜索",
                            "url": "http://www.soso.com/"
                        },
                        {
                            "type": "view",
                            "name": "测试",
                            "url": "http://v.qq.com/"
                        },
                        {
                            "type": "click",
                            "name": "好",
                            "key": "V1001_GOOD"
                        }]
                },
                {
                    "type": "click",
                    "name": "button2",
                    "key": "V1002_TODAY_MUSIC"
                }
            ]
        }

        url = ' https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % accesstoken
        response = requests.post(url, data=json.dumps(menu, ensure_ascii=False), verify=True)
        if response.status_code == 200:
            result = json.loads(response.content)
            logger.debug("the response is %s" % result)
            return result
        else:
            # throw exception
            pass
