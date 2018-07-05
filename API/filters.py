from itertools import chain

from rest_framework import filters

from Main.models import TreeCategory, District, Post, Currency, City


class PostCategoryFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		parameter = request.GET.get('quick_filter', default='all')
		if parameter == 'recommended':
			return queryset.filter(is_top=True)
		elif parameter == 'sale':
			return queryset.filter(
				category_tree__in=[branch.id for branch in
					queryset.filter(id=1).get_descendants(include_self=True)])
		elif parameter == 'rent':
			return queryset.filter(
				category_tree__in=[branch.id for branch in
					queryset.filter(id=7).get_descendants(include_self=True)])
		elif parameter == 'commercial':
			return queryset.filter(
				category_tree__in=[branch.id for branch in
					queryset.filter(id=13).get_descendants(include_self=True)])
		return queryset


class DistrictsFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		parameter = request.GET.get('city', default='all')
		if parameter != 'all':
			return queryset.filter(city=parameter)
		return queryset


class CitiesFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		parameter = request.GET.get('city', default=None)
		if parameter:
			return queryset.filter(id=int(parameter))
		return queryset


class PostCurrencyFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		cur_id = request.GET.get('currency_type', default=None)
		exchange = request.GET.get('exchange', default=None)
		summ_unexchanged = request.GET.get('summ', default=None)
		if not cur_id or not exchange or not summ_unexchanged:
			return queryset
		summ_unexchanged = float(summ_unexchanged)
		sum_exchanged = summ_unexchanged * float(exchange)
		posts = queryset
		currency = queryset
		first_posts = posts.filter(
			currency_type__in=[cur['id'] for cur in currency.filter(id=cur_id).values()]).filter(
			price__gte=summ_unexchanged)
		second_posts = posts.filter(
			currency_type__in=[cur['id'] for cur in currency.exclude(id=cur_id).values()]).filter(
			price__gte=sum_exchanged)
		queryset = list(chain(first_posts, second_posts))
		return queryset


class CategoryTreeFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		node = request.GET.get('category', default=None)
		if not node:
			return queryset
		node = int(node)
		queryset = queryset.filter(category_tree__in=[tree.id for tree in
			TreeCategory.objects.filter(id=node).get_descendants(include_self=True)])
		return queryset
