"""Custom pagination classes"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class StandardResultsPagination(PageNumberPagination):
    """Standard pagination for API responses"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('total_pages', self.page.paginator.num_pages),
            ('current_page', self.page.number),
            ('page_size', self.get_page_size(self.request)),
            ('results', data)
        ]))

class LargeResultsPagination(PageNumberPagination):
    """Pagination for large datasets"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200

class SmallResultsPagination(PageNumberPagination):
    """Pagination for small datasets"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
