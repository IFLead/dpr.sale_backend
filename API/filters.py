from rest_framework import filters
from Main.models import TreeCategory, District


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
