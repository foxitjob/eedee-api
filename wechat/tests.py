# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.test import TestCase
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
from django.core.wsgi import get_wsgi_application
from django.core.exceptions import ObjectDoesNotExist

application = get_wsgi_application()
from werobot import WeRoBot
from wechat import models as wechat_models
import json

# 测试号
# robot = WeRoBot(token='sdxvTQLlNhiEk9d8PsYzUpzToqUWMEoo')
# robot.config["APP_ID"] = "wx4c40f5900aa7efd0"
# robot.config["APP_SECRET"] = "eede69ee1c02a23f011f22f94f8d3905"

# 订阅号
robot = WeRoBot(token='sdxvTQLlNhiEk9d8PsYzUpzToqUWMEoo')
robot.config["APP_ID"] = "wx4c40f5900aa7efd0"
robot.config["APP_SECRET"] = "eede69ee1c02a23f011f22f94f8d3905"

client = robot.client
# print json.dumps(client.get_menu(), ensure_ascii=False)
# client.create_menu({
#     "button": [
#         {
#             "type": "click",
#             "name": u"今日歌曲",
#             "key": "V1001_TODAY_MUSIC"
#         },
#         {
#             "type": "click",
#             "name": u"歌手简介",
#             "key": "V1001_TODAY_SINGER"
#         },
#         {
#             "name": u"菜单",
#             "sub_button": [
#                 {
#                     "type": "view",
#                     "name": u"搜索",
#                     "url": "http://www.soso.com/"
#                 },
#                 {
#                     "type": "view",
#                     "name": u"视频",
#                     "url": "http://v.qq.com/"
#                 },
#                 {
#                     "type": "click",
#                     "name": u"赞一下我们",
#                     "key": "V1001_GOOD"
#                 }
#             ]
#         }
#     ]})
# print client.grant_token()
# print   client.get_ip_list()
# fans = client.get_followers()
#
# print json.dumps(client.get_users_info(fans['data']['openid'], lang='zh_CN'),ensure_ascii=False)
# print client.get_media_list(media_type="image", offset=0, count=20)
# print client.get_media_list("video", 0, 20)
# print client.get_media_list("voice", 0, 20)
# print client.get_media_count()
# medialist = client.get_media_list("news", 0, 6)
# print json.dumps(medialist,ensure_ascii=False, encoding="utf-8")
import time, datetime

def test001():
    medialist = client.get_media_list("news", 0, 20)
    print medialist
    print json.dumps(medialist)
    for material in medialist['item']:
        media_id = material.get('media_id')
        update_time = material.get('update_time')
        create_time = material['content'].get('create_time')
        material_ins = wechat_models.Material.objects.create(media_id=media_id,
                                                             update_time=update_time,
                                                             create_time=create_time,
                                                             type="news"
                                                             )
        for new in material['content']['news_item']:
            thumb_media_id = new.get('thumb_media_id')
            author = new.get('author')
            show_cover_pic = new.get('show_cover_pic')
            title = new.get('title').encode("latin1").decode("utf8")
            content_source_url = new.get('content_source_url')
            content = new.get('content').encode("latin1").decode("utf8")
            url = new.get('url')
            thumb_url = new.get('thumb_url')
            digest = new.get('digest').encode("latin1").decode("utf8")
            wechat_models.News.objects.create(thumb_media_id=thumb_media_id,
                                              author=author,
                                              show_cover_pic=show_cover_pic,
                                              title=title,
                                              content_source_url=content_source_url,
                                              content=content,
                                              url=url,
                                              thumb_url=thumb_url,
                                              digest=digest,
                                              material=material_ins,
                                              )


if __name__ == '__main__':
    test001()
    # timeStamp = 1381419600
    # print datetime.datetime.utcfromtimestamp(timeStamp)
    # print time.localtime(timeStamp)
    # from django.utils import timezone
    #
    # print timezone.now()
