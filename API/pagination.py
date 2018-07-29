from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PostLimitOffsetPagination(LimitOffsetPagination):
	default_limit = 8
	max_limit = 10


class PostPageNumberPagination(PageNumberPagination):
	page_size = 8

class PostPageAdminPagination(PageNumberPagination):
	page_size = 20
	page_size_query_param = 'limit'
	max_page_size = 300
