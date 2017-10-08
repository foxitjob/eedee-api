# -*- encoding: utf-8 -*-
from models import Product
from haystack import indexes


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    # 文章内容
    text = indexes.CharField(document=True, use_template=True)
    # 对name字段进行索引
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()