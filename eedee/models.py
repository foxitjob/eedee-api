# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

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
