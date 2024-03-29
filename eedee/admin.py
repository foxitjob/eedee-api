# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from django.contrib import admin
from models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources


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
    list_display_links = ('name',)
    ordering = ('category', 'id',)


class supplier_imagesInline(admin.TabularInline):
    # form = CityInlineForm
    model = Supplier.images.through
    extra = 3
    verbose_name = '经销商图片'
    verbose_name_plural = '经销商图片'
    # suit_classes = 'suit-tab suit-tab-cities'


class supplier_product_imagesInLine(admin.TabularInline):
    # form = CityInlineForm
    model = Supplier.product_images.through
    extra = 3
    verbose_name = '产品图片'
    verbose_name_plural = '产品图片'
    # suit_classes = 'suit-tab suit-tab-cities'


class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'content', 'product_introduce', 'buy_product', 'agent_product', 'sell_area', 'contact',
                  'contact_job_title', 'sale_phone', 'consult_phone', 'complain_phone', 'address',
                  'fax', 'email', 'website', 'is_free_inquiry',)
        skip_unchanged = True
        report_skipped = False


class SupplierAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'product_list', 'picture', 'is_free_inquiry')
    filter_horizontal = ('products',)
    inlines = (supplier_imagesInline, supplier_product_imagesInLine)
    list_display_links = ('name',)
    exclude = ('images', 'product_images')
    resource_class = SupplierResource


class ImagesInline(admin.TabularInline):
    # form = CityInlineForm
    model = Image
    extra = 3
    verbose_name_plural = '厂家图片'
    # suit_classes = 'suit-tab suit-tab-cities'


class manufacturer_imagesInline(admin.TabularInline):
    # form = CityInlineForm
    model = Manufacturer.images.through
    extra = 3
    verbose_name = '厂家图片'
    verbose_name_plural = '厂家图片'
    # suit_classes = 'suit-tab suit-tab-cities'


class manufacturer_product_imagesInLine(admin.TabularInline):
    # form = CityInlineForm
    model = Manufacturer.product_images.through
    extra = 3
    verbose_name = '产品图片'
    verbose_name_plural = '产品图片'
    # suit_classes = 'suit-tab suit-tab-cities'


class ManufacturerResource(resources.ModelResource):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name', 'content', 'product_introduce', 'contact',
                  'contact_job_title', 'sale_phone', 'consult_phone', 'complain_phone', 'address',
                  'fax', 'email', 'website', 'is_free_inquiry',)
        skip_unchanged = True
        report_skipped = False


class ManufacturerAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'product_list', 'picture', 'is_free_inquiry')
    filter_horizontal = ('products',)
    list_display_links = ('name',)
    inlines = (manufacturer_imagesInline, manufacturer_product_imagesInLine)
    exclude = ('images', 'product_images')
    resource_class = ManufacturerResource


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image')


# admin.site.register(Category2, Category2Admin)
# admin.site.register(Category1, Category1Admin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Image, ImageAdmin)
