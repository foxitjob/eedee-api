from django.shortcuts import render
# Create your views here.
import time
import hashlib
from django.views.generic.base import View
from django.http.response import HttpResponse
from django.core.exceptions import PermissionDenied
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ExampleView(APIView):
    def get(self, request, format=None):
        content = {
            'user': "123",  # `django.contrib.auth.User` instance.
            'auth': "456",  # None
        }
        return Response(content)


class WeixinInterface(View):
    token = 'z3W9EREM2s3M2x33ZH2S33ehRIXYR2yz'

    def validate(self, request, *args, **kwargs):
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        tmp_str = hashlib.sha1(''.join(sorted([self.token, timestamp, nonce]))).hexdigest()
        if tmp_str == signature:
            return True
        return False

    def get(self, request):
        if self.validate(request):
            return HttpResponse(request.GET.get('echostr', ''))
        raise PermissionDenied

    def post(self, request, *args, **kwargs):
        xml_str = request.body
        xml = ET.fromstring(xml_str)
        content = xml.find('Content').text
        msgType = xml.find('MsgType').text
        fromUserName = xml.find('FromUserName').text
        toUserName = xml.find('ToUserName').text
        createTime = xml.find('CreateTime').text
        print content, msgType, fromUserName, toUserName, createTime
        reply = """
            <xml>
            <ToUserName>%s</ToUserName>
            <FromUserName>%s</FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType>%s</MsgType>
            <Content>%s</Content>
            </xml>""" % (fromUserName, toUserName, str(int(time.time())), msgType, content)
        print reply
        return HttpResponse(reply, content_type="application/xml")

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeixinInterface, self).dispatch(*args, **kwargs)
