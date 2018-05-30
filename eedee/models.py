# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class Category1(MPTTModel):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
    is_active = models.BooleanField()
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories1"

    class MPTTMeta:
        order_insertion_by = ['order']

    def save(self, *args, **kwargs):
        super(Category1, self).save(*args, **kwargs)
        Category1.objects.rebuild()


class Category2(MPTTModel):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories2"

    class MPTTMeta:
        order_insertion_by = ['name']

    def save(self, *args, **kwargs):
        super(Category2, self).save(*args, **kwargs)
        Category2.objects.rebuild()


@python_2_unicode_compatible
class Category(MPTTModel):
    name = models.CharField('科室名称', max_length=100)
    slug = models.CharField('网址', max_length=32, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='是否激活')
    order = models.IntegerField('排列顺序', blank=True, null=True)

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

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        Category.objects.rebuild()

    class Meta:
        verbose_name = '科室分类'
        verbose_name_plural = '科室分类'


@python_2_unicode_compatible
class Image(models.Model):
    title = models.CharField('标题', max_length=100, blank=True, null=True)
    classify = models.CharField('分类', choices=[('product', 'Product'), ('manufacturer', 'Panufacturer')], max_length=50,
                                blank=True, null=True)
    image = models.ImageField('图片', upload_to='uploads/images', blank=True, null=True)
    created_on = models.DateTimeField('创建日期', auto_now_add=True)
    updated_on = models.DateTimeField('更新日期', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '图片库'
        verbose_name_plural = '图片库'
        # ordering = ['category', ]  # 按照哪个栏目排序


@python_2_unicode_compatible
class Product(models.Model):
    name = models.CharField('产品类别名称', max_length=100)
    category = models.ForeignKey(Category, verbose_name='科室分类', blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/product/images', blank=True, null=True, verbose_name='封面图片')

    def __str__(self):
        return self.name

    def show_picture(self):
        return format_html('<a href=/media/%s><img src=/media/%s></a>' % (self.picture, self.picture))

    def get_product_category_url(self):
        return reverse('product_category', args=(self.pk,))

    # def get_absolute_url(self):
    #     return reverse('product', args=(self.pk,))

    class Meta:
        verbose_name = '产品类别'
        verbose_name_plural = '产品类别'
        ordering = ['category', ]  # 按照哪个栏目排序


@python_2_unicode_compatible
class Supplier(models.Model):
    name = models.CharField('经销商名称', max_length=100)
    picture = models.ImageField(upload_to='uploads/supplier/images', blank=True, null=True, verbose_name='封面图片')
    images = models.ManyToManyField(Image, verbose_name='供应商图片', blank=True, related_name='supplier_images')
    product_images = models.ManyToManyField(Image, verbose_name='产品图片', blank=True,
                                            related_name='supplier_product_images')
    content = UEditorField('经销商介绍', height=300, width=680,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    products = models.ManyToManyField(Product, verbose_name='产品类别列表', blank=True)
    buy_product = models.CharField('求购产品', max_length=200, blank=True, null=True, )
    agent_product = models.CharField('代理产品', max_length=200, blank=True, null=True, )
    sell_area = models.CharField('负责区域', max_length=200, blank=True, null=True, )
    contact = models.CharField('联系人', max_length=200, blank=True, null=True, )
    contact_job_title = models.CharField('联系人职位', max_length=200, blank=True, null=True, )
    sale_phone = models.CharField('销售热线', max_length=50, blank=True, null=True, )
    consult_phone = models.CharField('咨询热线', max_length=50, blank=True, null=True, )
    complain_phone = models.CharField('投诉热线', max_length=50, blank=True, null=True, )
    address = models.CharField('地址', max_length=200, blank=True, null=True, )
    fax = models.CharField('传真', max_length=50, blank=True, null=True, )
    email = models.CharField('邮箱', max_length=50, blank=True, null=True, )
    website = models.URLField('企业官网', max_length=50, blank=True, null=True, )
    is_free_inquiry = models.BooleanField(verbose_name='是否免费查看信息', )

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
    picture = models.ImageField(upload_to='uploads/manufacturer/images', blank=True, null=True, verbose_name='封面图片')
    images = models.ManyToManyField(Image, verbose_name='厂家图片', blank=True,
                                    related_name='manufacturer_images')
    product_images = models.ManyToManyField(Image, verbose_name='产品图片', blank=True,
                                            related_name='manufacturer_product_images')
    content = UEditorField('厂家介绍', height=300, width=680,
                           default=u'', blank=True, null=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    product_introduce = models.TextField(verbose_name='产品介绍', blank=True, null=True, )
    products = models.ManyToManyField(Product, verbose_name='产品类别列表', blank=True, )
    contact = models.CharField('联系人', max_length=200, blank=True, null=True, )
    contact_job_title = models.CharField('联系人职位', max_length=200, blank=True, null=True, )
    sale_phone = models.CharField('销售热线', max_length=50, blank=True, null=True, )
    consult_phone = models.CharField('咨询热线', max_length=50, blank=True, null=True, )
    complain_phone = models.CharField('投诉热线', max_length=50, blank=True, null=True, )
    address = models.CharField('地址', max_length=200, blank=True, null=True, )
    fax = models.CharField('传真', max_length=50, blank=True, null=True, )
    email = models.CharField('邮箱', max_length=50, blank=True, null=True, )
    website = models.URLField('企业官网', max_length=50, blank=True, null=True, )
    is_free_inquiry = models.BooleanField(verbose_name='是否免费查看信息')

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
