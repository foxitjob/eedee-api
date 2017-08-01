# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *


# Create your views here.


def index(request):
    home_display_cout = Product.objects.count()
    home_display_product = Product.objects.all()[:5]
    category_list = {}
    categorys = Category.objects.filter(parent=None)
    # for category in categorys:
    #     category_name=category.name
    #     category_list.append()
    return render(request, 'index.html', {
        'home_display_cout': home_display_cout,
        'home_display_product': home_display_product,
        'categorys': categorys,
    })


def category_list(request, category_slug):
    category = Category.objects.get(slug=category_slug)

    return render(request, 'category_list.html', {
        'category': category,
    })
