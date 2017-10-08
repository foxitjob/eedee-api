# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.core.urlresolvers import reverse
from django.utils.html import format_html


# Create your models here.

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('科室名称', max_length=100)
    slug = models.CharField('网址', max_length=32, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    sequence = models.IntegerField('排列顺序', blank=True, null=True)

    def __str__(self):
        return self.name

    def is_parent(self):
        if self.category_set.all():
            return True
        else:
            return False

    def root_category(self):
        if self.parent:
            self = self.parent
            return self.root_category()
        else:
            return self.id

    is_parent.boolean = True

    def get_category_product_url(self):
        return reverse('category_product', args=(self.slug,))

    class Meta:
        # unique_together = ("slug", "parent")
        verbose_name = ''
        verbose_name_plural = '科室分类'


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField('产品名称', max_length=100)
    category = models.ForeignKey(Category)
    picture = models.ImageField(upload_to='uploads/product/images', blank=True, null=True)

    def __str__(self):
        return self.name

    def show_picture(self):
        return format_html('<a href=/media/%s><img src=/media/%s></a>' % (self.picture,self.picture))

    def get_product_category_url(self):
        return reverse('product_category', args=(self.pk,))

    # def get_absolute_url(self):
    #     return reverse('product', args=(self.pk,))

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['category', ]  # 按照哪个栏目排序


@python_2_unicode_compatible
class Supplier(models.Model):
    name = models.CharField('经销商名称', max_length=100)
    picture = models.ImageField(upload_to='uploads/supplier/images', blank=True, null=True)
    content = UEditorField('经销商介绍', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    products = models.ManyToManyField(Product, verbose_name='产品列表', )
    address = models.CharField('地址', max_length=200, blank=True)
    phone = models.CharField('电话', max_length=50, blank=True)
    fax = models.CharField('传真', max_length=50, blank=True)
    postcode = models.CharField('邮编', max_length=50, blank=True)

    def product_list(self):
        product_list = [product.name for product in self.products.all()]
        return format_html('<div>' + '</div><div>'.join(product_list) + '</div>')

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('supplier', args=(self.pk,))

    def get_supplier_product_url(self):
        return reverse('supplier_product', args=(self.pk,))

    class Meta:
        verbose_name = '经销商'
        verbose_name_plural = '经销商'
        # ordering = ['category', ]  # 按照哪个栏目排序


@python_2_unicode_compatible
class Manufacturer(models.Model):
    name = models.CharField('厂家名称', max_length=100)
    picture = models.ImageField(upload_to='uploads/manufacturer/images', blank=True, null=True)
    content = UEditorField('厂家介绍', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    products = models.ManyToManyField(Product, verbose_name='产品列表', )
    address = models.CharField('地址', max_length=200, blank=True)
    phone = models.CharField('电话', max_length=50, blank=True)
    fax = models.CharField('传真', max_length=50, blank=True)
    postcode = models.CharField('邮编', max_length=50, blank=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('manufacturer', args=(self.pk,))

    def product_list(self):
        product_list = [product.name for product in self.products.all()]
        return format_html('<div>' + '</div><div>'.join(product_list) + '</div>')

    class Meta:
        verbose_name = '厂家'
        verbose_name_plural = '厂家'
        # ordering = ['category', ]  # 按照哪个栏目排序
