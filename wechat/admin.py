# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib import messages
import models
import werobot
from common import GenPassword
import robot
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.admin import AdminSite
from models import Fans
import logging

info_logger = logging.getLogger('django.info')
error_logger = logging.getLogger('django.error')


class MyAdminSite(AdminSite):
    site_header = 'Monty Python administration'


admin_site = MyAdminSite(name='myadmin')
admin_site.register(Fans)


# def export_selected_objects(modeladmin, request, queryset):
#     selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
#     ct = ContentType.objects.get_for_model(queryset.model)
#     return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))


# Register your models here.

# admin.site.add_action(export_selected_objects, 'export_selected')


class AdminMenu(admin.ModelAdmin):
    list_display = ('id', 'name', 'content', 'update_time', 'active')
    actions = ['pull_menu', 'push_menu']

    def pull_menu(self, request, queryset):
        queryset.update(status="free", hostname="")

    pull_menu.short_description = "更新到本地"

    def push_menu(self, request, queryset):
        print queryset.get().name

    push_menu.short_description = "更新到服务器"


class AdminWechat(admin.ModelAdmin):
    list_display = ('id', 'name', 'appid', 'appsecret', 'asekey', 'accesstoken', 'token', 'expires_in', 'update_time')
    actions = ['refresh_accesstoken', 'generate_token']

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'appid', 'appsecret', 'asekey', )
    #     }),
    #     ('Advanced options', {
    #         'classes': ('collapse',),
    #         'fields': ('token',),
    #     }),
    # )

    def refresh_accesstoken(self, request, queryset):
        msg = ''
        for wechat in queryset.all():
            robot = werobot.WeRoBot(token=wechat.token)
            robot.config["APP_ID"] = wechat.appid
            robot.config["APP_SECRET"] = wechat.appsecret
            client = robot.client
            grant_token = client.grant_token()
            access_token = grant_token.get('access_token')
            expires_in = grant_token.get('expires_in')
            wechat.accesstoken = access_token
            wechat.expires_in = expires_in
            wechat.save()
            msg += "获取%s的AccessToken成功 " % wechat.name
        self.message_user(request, msg, level=messages.INFO)

    refresh_accesstoken.short_description = "获取AccessToken"

    def generate_token(self, request, queryset):
        msg = ''
        for wechat in queryset.all():
            wechat.token = GenPassword(32)
            wechat.save()
            msg += "生成%s的Token成功 " % wechat.name
        self.message_user(request, msg, level=messages.INFO)

    generate_token.short_description = "创建Token"


class AdminGroup(admin.ModelAdmin):
    list_display = ('id', 'name', 'count',)
    actions = None

    # list_editable = ['name', ]

    def save_model(self, request, obj, form, change):
        client = robot.robot.client
        if not obj.id:
            response = client.create_group(obj.name)
            info_logger.info("create group %s, the response is %s" % (obj.name, response))
            obj.id = response['group']['id']
            obj.name = response['group']['name']
            super(AdminGroup, self).save_model(request, obj, form, change)
        else:
            client.update_group(obj.id, obj.name)
            info_logger.info("update group %s name to %s" % (obj.id, obj.name))
            super(AdminGroup, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        client = robot.robot.client
        client.delete_group(obj.id)
        info_logger.info("delete group %s" % obj.id)
        super(AdminGroup, self).delete_model(request, obj)


class AdminFans(admin.ModelAdmin):
    list_display = (
        'subscribe', 'openid', 'nickname', 'get_sex', 'city', 'country', 'province', 'language', 'get_headimgurl',
        'get_subscribe_time', 'remark', 'groupid')
    actions = ['send_text_message']
    list_filter = ('groupid',)
    list_display_links = ('openid',)

    def save_model(self, request, obj, form, change):
        client = robot.robot.client
        client.move_user(obj.openid, obj.groupid.id)
        info_logger.info("move user %s to group %s" % (obj.nickname, obj.groupid.name))
        super(AdminFans, self).save_model(request, obj, form, change)

    # 发送文本消息
    def send_text_message(self, request, queryset):
        openids = [fans.openid for fans in queryset]
        return HttpResponseRedirect("/wechat/send_text_message/?openids=%s" % ','.join([openid for openid in openids]))

    send_text_message.short_description = "发送文本消息"


class AdminMaterial(admin.ModelAdmin):
    list_display = (
        'media_id', 'get_news', 'type', 'get_update_time', 'get_create_time',)


class AdminNews(admin.ModelAdmin):
    list_display = (
        'thumb_media_id', 'author', 'show_cover_pic', 'title', 'get_thumb_url',
        'digest', 'material')
    # actions = ['refresh_accesstoken', 'generate_token']


admin.site.register(models.Menu, AdminMenu)
admin.site.register(models.Wechat, AdminWechat)
admin.site.register(models.Group, AdminGroup)
admin.site.register(models.Fans, AdminFans)
admin.site.register(models.News, AdminNews)
admin.site.register(models.Material, AdminMaterial)
