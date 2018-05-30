# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from models import *


# Register your models here.

# class Category1Admin(MPTTModelAdmin, SortableModelAdmin):
#     """
#     Example of django-mptt and sortable together. Important note:
#     If used together MPTTModelAdmin must be before SortableModelAdmin
#     """
#     mptt_level_indent = 20
#     search_fields = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ('name', 'slug', 'is_active')
#     list_editable = ('is_active',)
#     list_display_links = ('name',)
#     sortable = 'order'
#
#
# class Category2Admin(MPTTModelAdmin):
#     """
#     Example of django-mptt and sortable together. Important note:
#     If used together MPTTModelAdmin must be before SortableModelAdmin
#     """
#     mptt_level_indent = 20
#     search_fields = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}
#     list_display = ('name', 'slug',)
#     list_display_links = ('name',)


class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_editable = ('is_active', 'order')
    list_display = ('name', 'slug', 'is_active', 'order')
    list_display_links = ('name',)


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


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'classify', 'image')
    list_filter = ('classify',)


# admin.site.register(Category2, Category2Admin)
# admin.site.register(Category1, Category1Admin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Image, ImageAdmin)
