# -*- coding: utf-8 -*-

import werobot
from models import Wechat


wechat = Wechat.objects.get()
robot = werobot.WeRoBot(token=wechat.token)
robot.config["APP_ID"] = wechat.appid
robot.config["APP_SECRET"] = wechat.appsecret

@robot.image
def hello(message):
    return message.img

@robot.subscribe
def subscribe(message):
    return 'Hello My Friend!'

@robot.text
def hello(message):
    return robot.ge
    return message.content

@robot.key_click("music")
def music(message):
    return '你点击了“今日歌曲”按钮'

@robot.filter("a")
def a():
    return "正文为 a "

import re

@robot.filter(re.compile(".*?bb.*?"))
def b():
    return "正文中含有 b "

@robot.filter(re.compile(".*?c.*?"), "d")
def c():
    return "正文中含有 c 或正文为 d"

# token 来自微信公众平台, 需要配置
# robot = werobot.WeRoBot(token='sdxvTQLlNhiEk9d8PsYzUpzToqUWMEoo')
# robot.config["APP_ID"] = "wx4c40f5900aa7efd0"
# robot.config["APP_SECRET"] = "eede69ee1c02a23f011f22f94f8d3905"

#
# @robot.image
# def hello(message):
#     return message.img
#
#
# @robot.subscribe
# def subscribe(message):
#     return 'Hello My Friend!'
#
#
# @robot.text
# def hello(message):
#     client = robot.client
#     client.create_menu({
#         "button": [{
#             "type": "click",
#             "name": u"明日歌曲",
#             "key": "music"
#         }]
#     })
#     return message.content
#
#
# @robot.key_click("music")
# def music(message):
#     return '你点击了“今日歌曲”按钮'
#
#
# @robot.filter("a")
# def a():
#     return "正文为 a "
#
#
# import re
#
#
# @robot.filter(re.compile(".*?bb.*?"))
# def b():
#     return "正文中含有 b "
#
#
# @robot.filter(re.compile(".*?c.*?"), "d")
# def c():
#     return "正文中含有 c 或正文为 d"
