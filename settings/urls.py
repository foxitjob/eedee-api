# -*- coding: utf-8 -*-
"""eedee_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.conf.urls.static import static
import settings
import eedee.views
import eedee.search_views as search_views

admin.site.site_header = '互联力量CMS'
admin.site.site_title = '互联力量CMS'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls'),),
    url(r'^$', eedee.views.index, name='index'),
    # url(r'^eedee/index1', eedee.views.index1),
    url(r'^eedee/category_product/(?P<category_slug>[^/]+)/$', eedee.views.category_product, name='category_product'),
    # url(r'^eedee/product_category/(?P<produc_id>[^/]+)/$', eedee.views.product_category_list, name='product_category'),
    url(r'^eedee/product_manufacturer/(?P<produc_id>[^/]+)/$', eedee.views.product_manufacturer, name='product_manufacturer'),
    url(r'^eedee/product_supplier/(?P<produc_id>[^/]+)/$', eedee.views.product_supplier, name='product_supplier'),
    url(r'^eedee/manufacturer/(?P<id>[^/]+)/$', eedee.views.manufacturer_detail, name='manufacturer_detail'),
    url(r'^eedee/supplier/(?P<id>[^/]+)/$', eedee.views.supplier_detail, name='supplier_detail'),
    url(r'^search_test/', include('haystack.urls')),
    url(r'^search/', search_views.MySeachView(), name='haystack_search'),
    url('^api/', include('api.urls', namespace='api')),
]
urlpatterns += staticfiles_urlpatterns()


urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
