# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from models import *


# Register your models here.

class Category1Admin(MPTTModelAdmin, SortableModelAdmin):
    mptt_level_indent = 20
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)
    # Specify name of sortable property
    sortable = 'order'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'sequence', 'is_parent', 'root_category')
    ordering = ('id',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'picture')
    list_filter = ('category',)
    ordering = ('id',)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_list', 'picture')
    filter_horizontal = ('products',)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'product_list', 'picture')
    filter_horizontal = ('products',)


admin.site.register(Category1, Category1Admin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
