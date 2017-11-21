from eedee.models import *
import rest_framework_filters as filters

class ManufacturerFilter(filters.FilterSet):
    class Meta:
        model = Manufacturer
        fields = ['phone', 'fax', 'postcode']

class SupplierFilter(filters.FilterSet):
    class Meta:
        model = Supplier
        fields = ['phone', 'fax', 'postcode']