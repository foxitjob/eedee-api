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
from rest_framework.permissions import AllowAny
from django.core.urlresolvers import reverse
from rest_framework import viewsets
import rest_framework_filters as filters
from rest_framework.decorators import detail_route, list_route
from eedee.models import *
from serializers import *
from filters import *
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200


class ManufacturerViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, add, update or delete Manufacturer.
    """
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    filter_class = ManufacturerFilter
    pagination_class = StandardResultsSetPagination

    @list_route(methods=['get'], url_path='detail')
    def list_detail(self, request, *args, **kwargs):
        """
        List Datacenter with detail information.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ManufacturerDetailSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='detail')
    def detail(self, request, pk=None):
        """
        Retrieve Datacenter with detail information.
        """
        queryset = Manufacturer.objects.get(pk=pk)
        data = ManufacturerDetailSerializer(queryset).data
        return Response(data)


class SupplierViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, add, update or delete Supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_class = SupplierFilter
    pagination_class = StandardResultsSetPagination

    @list_route(methods=['get'], url_path='detail')
    def list_detail(self, request, *args, **kwargs):
        """
        List Supplier with detail information.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = SupplierDetailSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='detail')
    def detail(self, request, pk=None):
        """
        Retrieve Supplier with detail information.
        """
        queryset = Supplier.objects.get(pk=pk)
        data = SupplierDetailSerializer(queryset).data
        return Response(data)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, add, update or delete Supplier.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_class = CategoryFilter
    pagination_class = StandardResultsSetPagination

    @list_route(methods=['get'], url_path='detail')
    def list_detail(self, request, *args, **kwargs):
        """
        List Supplier with detail information.
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CategoryDetailSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CategoryDetailSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='detail')
    def detail(self, request, pk=None):
        """
        Retrieve Supplier with detail information.
        """
        queryset = Category.objects.get(pk=pk)
        data = CategoryDetailSerializer(queryset).data
        return Response(data)

class ApiRootView(APIView):
    # authentication_classes = []
    permission_classes = (AllowAny,)
    view_name = 'REST API'

    def get(self, request, format=None):
        """ List supported API versions. """
        current = reverse('api:api_root_view', args=[]) + 'v1'
        data = dict(description='EEDEE REST API', current_version=current, available_versions=dict(v1=current))
        return Response(data)


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
