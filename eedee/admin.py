# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


# Register your models here.

class CatelogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent', 'sequence', 'is_parent', 'root_category')
    ordering = ('id',)


admin.site.register(Category, CatelogAdmin)
