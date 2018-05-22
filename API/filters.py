from itertools import chain

from rest_framework import filters

from Main.models import TreeCategory, District, Post, Currency


class PostCategoryFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		parameter = request.GET.get('quick_filter', default='all')
		if parameter == 'recommended':
			return queryset.filter(is_top=True)
		elif parameter == 'sale':
			return queryset.filter(
				category_tree__in=[branch.id for branch in
					TreeCategory.objects.filter(id=1).get_descendants(include_self=True)])
		elif parameter == 'rent':
			return queryset.filter(
				category_tree__in=[branch.id for branch in
					TreeCategory.objects.filter(id=7).get_descendants(include_self=True)])
		elif parameter == 'commercial':
			return queryset.filter(
				category_tree__in=[branch.id for branch in
					TreeCategory.objects.filter(id=13).get_descendants(include_self=True)])
		return queryset


class DistrictsFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		parameter = request.GET.get('city', default='all')
		if parameter != 'all':
			return District.objects.filter(city=parameter)
		return queryset


class PostCurrencyFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		symbol = request.GET.get('symbol', default='all')
		exchange = request.GET.get('exchange', default='all')
		summ_unexchanged = request.GET.get('summ', default='all')
		if symbol == 'all' or exchange == 'all' or summ_unexchanged == 'all':
			return queryset
		summ_unexchanged = float(summ_unexchanged)
		sum_exchanged = summ_unexchanged * float(exchange)
		first_posts = Post.objects.filter(currency_type__in=[cur['id'] for cur in Currency.objects.filter(symbol=symbol).values()]).filter(
			price__gte=summ_unexchanged)
		second_posts = Post.objects.filter(currency_type__in=[cur['id'] for cur in Currency.objects.exclude(symbol=symbol).values()]).filter(
			price__gte=sum_exchanged)
		queryset = list(chain(first_posts, second_posts))
		return queryset


class CategoryTreeFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		node = request.GET.get('node', default='all')
		node_in = request.GET.get('node', default='all')
		if node == 'all' or node_in == 'all':
			return queryset
		return queryset
