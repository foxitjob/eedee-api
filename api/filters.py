from eedee.models import *
import rest_framework_filters as filters


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'category']


class ManufacturerFilter(filters.FilterSet):
    class Meta:
        model = Manufacturer
        fields = []


class SupplierFilter(filters.FilterSet):
    class Meta:
        model = Supplier
        fields = []


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name', 'parent']
