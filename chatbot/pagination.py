"""Custom pagination class. We had to use this because we needed it for certain views and not globally.
The default DRF pagination plugin did not allow for our needs. The implementation is used in the views.py
files of the different modules."""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 15

class CustomPagination(PageNumberPagination):
    """Custom Pagination class to reduce the number of items gotten based on requests."""
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)), # can not set default = self.page
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })