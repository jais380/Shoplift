from rest_framework.pagination import PageNumberPagination

class ProductPagination(PageNumberPagination):

    page_size = 5
    page_query_param = 'page'

class ChartItemPagination(PageNumberPagination):

    page_size = 10
    page_query_param = 'page'
