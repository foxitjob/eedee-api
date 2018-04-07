from django.conf.urls import include, url
from views import *
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='EEDEE API')
v1_apiRouter = routers.DefaultRouter(trailing_slash=False)
v1_apiRouter.register(r'manufacturers', ManufacturerViewSet, 'manufacturers')
v1_apiRouter.register(r'suppliers', SupplierViewSet, 'suppliers')
v1_apiRouter.register(r'categories', CategoryViewSet, 'categories')

urlpatterns = [
    url('^$', ApiRootView.as_view(), name='api_root_view'),
    url(r'^docs', schema_view),
    url('^v1/', include(v1_apiRouter.urls))
]
