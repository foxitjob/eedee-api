# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from models import *


# Create your views here.


def index(request):
    home_display_cout = Product.objects.count()
    home_display_product = Product.objects.all()[:5]
    categorys = Category.objects.filter(parent=None).order_by('sequence')
    category_1 = categorys[0]
    category_2 = categorys[1]
    category_3 = categorys[2]
    category_4 = categorys[4]

    return render(request, 'index.html', {
        'home_display_cout': home_display_cout,
        'home_display_product': home_display_product,
        'categorys': categorys,
        'category_1': category_1,
        'category_2': category_2,
        'category_3': category_3,
        'category_4': category_4
    })


def index1(request):
    home_display_cout = Product.objects.count()
    home_display_product = Product.objects.all()[:5]
    category_list = {}
    categorys = Category.objects.filter(parent=None)
    # for category in categorys:
    #     category_name=category.name
    #     category_list.append()
    return render(request, 'index1.html', {
        'home_display_cout': home_display_cout,
        'home_display_product': home_display_product,
        'categorys': categorys,
    })


def category_product(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = category.product_set.all()
    # if not category.parent:
    #     categorys = category.category_set.all()
    #     for category in categorys:
    #         products += category.product_set.all()

    return render(request, 'category_product.html', {
        'category': category,
        'products': products,
        'advertisement': False
    })


def product_manufacturer(request, produc_id):
    product = get_object_or_404(Product, pk=produc_id)
    manufacturers = product.manufacturer_set.all()
    if product.category.parent:
        categorys = product.category.parent.category_set.all()
    else:
        categorys = product.category.category_set.all()

    return render(request, 'product_manufacturer.html', {
        'manufacturers': manufacturers,
        'categorys': categorys,
        'advertisement': False,
        'recommand':False
    })


def product_supplier(request, produc_id):
    product = get_object_or_404(Product, pk=produc_id)
    suppliers = product.supplier_set.all()
    if product.category.parent:
        categorys = product.category.parent.category_set.all()
    else:
        categorys = product.category.category_set.all()

    return render(request, 'product_supplier.html', {
        'suppliers': suppliers,
        'categorys': categorys,
        'advertisement': False,
        'recommand':False
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


def supplier_detail(request, id):
    supplier = get_object_or_404(Supplier, pk=id)

    return render(request, 'supplier.html', {
        'supplier': supplier,
    })
