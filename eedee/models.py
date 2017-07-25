# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.core.urlresolvers import reverse


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

    class Meta:
        # unique_together = ("slug", "parent")
        verbose_name = ''
        verbose_name_plural = '科室分类'


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField('产品名称', max_length=100)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', args=(self.pk,))

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ['category', ]  # 按照哪个栏目排序


@python_2_unicode_compatible
class Supplier(models.Model):
    name = models.CharField('经销商名称', max_length=100)
    content = UEditorField('经销商介绍', height=300, width=1000,
                 default=u'', blank=True, imagePath="uploads/images/",
                 toolbars='besttome', filePath='uploads/files/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('supplier', args=(self.pk,))

    class Meta:
        verbose_name = '经销商'
        verbose_name_plural = '经销商'
        # ordering = ['category', ]  # 按照哪个栏目排序


@python_2_unicode_compatible
class Manufacturer(models.Model):
    name = models.CharField('厂家名称', max_length=100)
    content = UEditorField('厂家介绍', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('manufacturer', args=(self.pk,))

    class Meta:
        verbose_name = '厂家'
        verbose_name_plural = '厂家'
        # ordering = ['category', ]  # 按照哪个栏目排序
