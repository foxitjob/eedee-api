# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from common import GenPassword
from django.utils.html import format_html
import time, datetime


# Create your models here.

class Menu(models.Model):
    name = models.CharField('名字', max_length=48, blank=False, )
    content = models.TextField('内容', blank=False)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    active = models.BooleanField('激活', default=True)

    # parentid = models.IntegerField('父菜单', null=False, default=0, )
    # name = models.CharField('名字', max_length=48, blank=False, )
    # typeid = models.SmallIntegerField('类型ID', null=False, default=1)
    # value = models.CharField('菜单值', max_length=128, blank=True)
    # keywvord = models.CharField('关键子', max_length=128, )
    # url = models.URLField('网址', Blank=True)
    # redirect_url = models.URLField('授权网址', Blank=True)
    # event = models.CharField('事件', max_length=64, Blank=True)
    # telphone = models.CharField('电话号码', max_length=32, Blank=True)
    # locatinon = models.CharField('定位', max_length=64, Blank=True)
    # orderby = models.SmallIntegerField('排序', null=False, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单'
        ordering = ['update_time']  # 按照哪个栏目排序


class Wechat(models.Model):
    name = models.CharField(max_length=32, blank=False)
    appid = models.CharField(max_length=18, blank=False)
    appsecret = models.CharField(max_length=32, blank=False)
    asekey = models.CharField(max_length=64, blank=True)
    token = models.CharField(max_length=32, default=GenPassword(32))
    accesstoken = models.CharField(max_length=512, blank=True)
    expires_in = models.IntegerField(null=True, editable=False, blank=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '公众号'
        verbose_name_plural = '公众号'


class Group(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    name = models.CharField(max_length=32, blank=False)
    count = models.IntegerField(editable=False, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '分组'
        verbose_name_plural = '分组'


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, blank=False)
    count = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '分组'
        verbose_name_plural = '分组'


class Fans(models.Model):
    subscribe = models.BooleanField()
    openid = models.CharField(primary_key=True, max_length=64, )
    nickname = models.CharField(max_length=64, blank=True)
    sex = models.SmallIntegerField()
    city = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True)
    province = models.CharField(max_length=32, blank=True)
    language = models.CharField(max_length=32, blank=True)
    headimgurl = models.URLField(blank=True)
    subscribe_time = models.IntegerField()
    remark = models.CharField(max_length=32, blank=True)
    groupid = models.ForeignKey(Group)

    def __unicode__(self):
        return self.openid

    class Meta:
        verbose_name = '粉丝'
        verbose_name_plural = '粉丝'

    def get_sex(self):
        if self.sex == 1:
            return "男"
        elif self.sex == 2:
            return "女"
        else:
            return ""

    def get_headimgurl(self):
        return format_html(
            '<img src = {} width=40px, high=40px>',
            self.headimgurl,
        )

    def get_subscribe_time(self):
        return datetime.datetime.fromtimestamp(self.subscribe_time).strftime("%Y-%m-%d %H:%M:%S")


class Material(models.Model):
    types = ["news", "image", "voice", "video"]
    types = ([tuple([type, type]) for type in types])
    media_id = models.CharField(max_length=100, unique=True)
    update_time = models.IntegerField()
    create_time = models.IntegerField()
    type = models.CharField(max_length=100, choices=types)

    def get_update_time(self):
        return datetime.datetime.fromtimestamp(self.update_time).strftime("%Y-%m-%d %H:%M:%S")

    def get_create_time(self):
        return datetime.datetime.fromtimestamp(self.create_time).strftime("%Y-%m-%d %H:%M:%S")

    def get_news(self):
        string = format_html("")
        for new in self.news_set.all():
            string += format_html(
                '<li><img src="{}" height="80" width="130"><a href="{}">{}</a></li>',
                new.thumb_url,
                new.url,
                new.title,
            )
        return string

    def __unicode__(self):
        return self.media_id

    class Meta:
        verbose_name = '永久素材'
        verbose_name_plural = '永久素材'


class News(models.Model):
    thumb_media_id = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=False)
    show_cover_pic = models.BooleanField()
    title = models.CharField(max_length=100, blank=False)
    content_source_url = models.URLField()
    content = models.TextField(blank=True)
    url = models.URLField()
    thumb_url = models.URLField()
    digest = models.CharField(max_length=100, blank=False)
    material = models.ForeignKey(Material)

    def get_thumb_url(self):
        return format_html(
            '<img src = {} width=40px, high=40px>',
            self.thumb_url,
        )

    def __unicode__(self):
        return self.thumb_media_id

    class Meta:
        verbose_name = '图文素材'
        verbose_name_plural = '图文素材'
