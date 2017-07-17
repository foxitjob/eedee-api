# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import models
import robot
import logging
import json

info_logger = logging.getLogger('django.info')
error_logger = logging.getLogger('django.error')


# Create your views here.

# @staff_member_required
# def my_admin_view(request):
#     return render_to_response('my_template.html',
#                               context_instance=RequestContext(request))

# def index(request):
#     latest_question_list = models.Fans.objects.order_by('-subscribe_time')[:5]
#     return HttpResponse(output)


def refreshgroup(request):
    groups_local = models.Group.objects.all()
    groupids_local = [group.id for group in groups_local]
    info_logger.info("groupids_local: %s", groupids_local)
    client = robot.robot.client
    # print client.get_groups()
    groups = client.get_groups().get('groups')
    groupids = [group.get('id') for group in groups]
    info_logger.info("groupids: %s", groupids)
    ret_ids = [item for item in groupids_local if item not in groupids]
    info_logger.info("ret_ids: %s", ret_ids)

    # 删除本地数据库不存在的group
    if ret_ids:
        models.Group.objects.filter(id__in=ret_ids).delete()

    for group in groups:
        if group.get('id') in groupids_local:
            group_local = models.Group.objects.get(id=group.get('id'))
            group_local.name = group.get('name')
            group_local.count = group.get('count')
            group_local.save()
            info_logger.info("update group: %s" % group_local)
        else:
            group_local = models.Group.objects.create(id=group.get('id'), name=group.get('name'),
                                                      count=group.get('count'))
            info_logger.info("create group: %s" % group_local)
    return HttpResponseRedirect("/admin/wechat/group")


def refreshfans(request):
    fanses_local = models.Fans.objects.all()
    openids_local = [fans.openid for fans in fanses_local]
    info_logger.info("openids_local: %s", openids_local)
    client = robot.robot.client
    client.ge
    # print client.get_followers()
    openids = client.get_followers(first_user_id=None).get('data').get('openid')
    info_logger.info("openids: %s", openids)
    ret_ids = [item for item in openids_local if item not in openids]
    info_logger.info("ret_ids: %s", ret_ids)
    # 删除本地数据库不存在的openid
    if ret_ids:
        models.Fans.objects.filter(openids__in=ret_ids).delete()

    users = client.get_users_info(openids, lang='zh_CN')
    # print users
    for user in users['user_info_list']:
        if user.get('openid') in openids_local:
            fans = models.Fans.objects.get(openid=user.get('openid'))
            fans.subscribe = user.get('subscribe')
            # openid=user.get('openid'),
            fans.nickname = user.get('nickname')
            fans.sex = user.get('sex')
            fans.city = user.get('city')
            fans.country = user.get('country')
            fans.province = user.get('province')
            fans.language = user.get('language')
            fans.headimgurl = user.get('headimgurl')
            fans.subscribe_time = user.get('subscribe_time')
            fans.remark = user.get('remark')
            fans.groupid = models.Group.objects.get(id=user.get('groupid'))
            fans.save()
            info_logger.info("update fans: %s" % fans)
        else:
            fans = models.Fans.objects.create(subscribe=user.get('subscribe'),
                                              openid=user.get('openid'),
                                              nickname=user.get('nickname'),
                                              sex=user.get('sex'),
                                              city=user.get('city'),
                                              country=user.get('country'),
                                              province=user.get('province'),
                                              language=user.get('language'),
                                              headimgurl=user.get('headimgurl'),
                                              subscribe_time=user.get('subscribe_time'),
                                              remark=user.get('remark'),
                                              groupid=models.Group.objects.get(id=user.get('groupid')))
            info_logger.info("create fans: %s" % fans)
    return HttpResponseRedirect("/admin/wechat/fans/")


def send_text_message(request):
    if request.POST:
        # return HttpResponse("OK")
        openids = request.POST['openids']
        openids = openids.split(',')
        content = request.POST['content']
        client = robot.robot.client
        success = 0
        success_fans_id = []
        for user_id in openids:
            try:
                result = client.send_text_message(user_id, content)
                info_logger.info(result)
                success += 1
                success_fans_id.append(user_id)
            except Exception, e:
                error_logger.error(e)
        data = {'total': len(openids),
                'success_count': success,
                'success': [fans.nickname for fans in models.Fans.objects.filter(openid__in=success_fans_id)],
                'failed': [fans.nickname for fans in
                           models.Fans.objects.filter(openid__in=openids).exclude(openid__in=success_fans_id)]}
        info_logger.info(data)
        return HttpResponse(json.dumps(data, ensure_ascii=False))
        # return HttpResponseRedirect("/admin/wechat/fans/")

    else:
        openids = request.GET.get('openids')
        return render(request, "wechat/send_text_message.html", {'openids': openids})
