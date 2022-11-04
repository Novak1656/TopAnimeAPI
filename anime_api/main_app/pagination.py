from rest_framework.pagination import PageNumberPagination


class AnimePaginationClass(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    max_page_size = 10


class GenrePaginationClass(PageNumberPagination):
    page_size = 25
    page_query_param = 'page'
    max_page_size = 25


class StudioPaginationClass(PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    max_page_size = 50
