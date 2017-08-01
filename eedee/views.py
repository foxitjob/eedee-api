# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
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


def category_product_list(request, category_slug):
    category = get_object_or_404(Category,slug=category_slug)

    return render(request, 'category_product_list.html', {
        'category': category,
    })


def product_category_list(request, produc_id):
    product = get_object_or_404(Product, pk=produc_id)

    return render(request, 'product_manufacturer_supplier.html', {
        'product': product,
    })


def manufacturer_detail(request, id):
    manufacturer = get_object_or_404(Manufacturer, pk=id)

    return render(request, 'manufacturer.html', {
        'manufacturer': manufacturer,
    })


def supplier_detail(request, produc_id):
    supplier = get_object_or_404(Supplier, pk=id)

    return render(request, 'supplier.html', {
        'supplier': supplier,
    })
