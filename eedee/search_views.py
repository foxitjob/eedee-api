# -*- encoding: utf-8 -*-
from haystack.views import SearchView


class MySeachView(SearchView):
    template = 'product_search.html'
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        context = super(MySeachView, self).extra_context()
        # side_list = Topic.objects.filter(kind='major').order_by('add_date')[:8]
        # context['side_list'] = side_list
        context['advertisement'] = False
        return context
