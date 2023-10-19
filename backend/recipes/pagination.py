from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"  # Изменил на 'page_size'
    max_page_size = 100
    recipes_limit_query_param = "recipes_limit"
