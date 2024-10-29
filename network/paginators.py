from rest_framework.pagination import PageNumberPagination


class NetworkPaginator(PageNumberPagination):
    """пагинатор для объектов сети"""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_description = "Номер страницы"
    page_size_query_description = "Кол-во объектов на странице"
