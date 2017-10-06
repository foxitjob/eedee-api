# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


# Register your models here.

class CatelogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'sequence', 'is_parent', 'root_category')
    ordering = ('id',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'picture')
    list_filter = ('category',)
    ordering = ('id',)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_list')
    filter_horizontal = ('products',)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_list')
    filter_horizontal = ('products',)


admin.site.register(Category, CatelogAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
