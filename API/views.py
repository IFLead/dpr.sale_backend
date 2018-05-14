import re

import json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from filer.models import File
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework import filters
from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView
)
from rest_framework.permissions import (
	IsAuthenticated,
)
from rest_framework.response import Response

from Main.models import Post, Category, Currency, TreeCategory, State, Window, Material, City, District, CustomData
from .filters import PostCategoryFilter, DistrictsFilter
from .pagination import PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, PostUpdateSerializer, CategorySerializer, CurrencySerializer, \
	TreeCategorySerializer, WindowSerializer, MaterialSerializer, StateSerializer, SinglePostSerializer, CitySerializer, \
	DistrictSerializer, UserSerializer


def districts(request):
	return JsonResponse(list(District.objects.filter(city_id__exact=request.GET['city_id']).values('id', 'name')),
		safe=False)


@staff_member_required
def top_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		post.is_top = True
		post.save()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def untop_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		post.is_top = False
		post.save()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def verify_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		post.verified = True
		post.save()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def unverify_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		post.verified = False
		post.save()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@login_required
def close_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		if request.user.is_active and (request.user.is_staff or post.owner.id == request.user.id):
			post.closed = True
			post.reason = request.POST['commentary']
			post.save()
			return JsonResponse({'status': 'OK', 'message': 'success'})
		else:
			return JsonResponse({'status': 'error', 'message': 'you have not access'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@login_required
def restore_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		if request.user.is_active and (request.user.is_staff or post.owner.id == request.user.id):
			post.closed = False
			post.reason = ''
			post.save()
			return JsonResponse({'status': 'OK', 'message': 'success'})
		else:
			return JsonResponse({'status': 'error', 'message': 'you have not access'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def delete_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		post.delete()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def verify_user(request):
	try:
		user = CustomData.objects.get(user_id__exact=request.POST['user_id'])
		user.verified = True
		user.user.save()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except CustomData.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def unverify_user(request):
	try:
		user = CustomData.objects.get(user_id__exact=request.POST['user_id'])
		user.user.delete()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except CustomData.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


def rename_dict_keys(d, names: dict, commercial: list, rent: list, sale: list):
	for k, v in names.items():
		if k in d:
			d[v] = d.pop(k)
		if 'filter' in d:
			val = d.pop('filter')
			d['category_id__in'] = commercial if val == 'commercial' else (rent if val == 'rent' else sale)
		if 'important' in d:
			val = d.pop('important').lower() == 'true'
			d['is_important'] = val


def search(request):
	names = {'city': 'district__city', 'min_square': 'square__gte', 'max_square': 'square__lte',
		'min_walls': 'rooms__gte', 'max_walls': 'rooms__lte', 'min_floor': 'floor__gte', 'max_floor': 'floor__lte',
		'min_price': 'price__gte', 'max_price': 'price__lte', }
	commercial = [10, 11, 13]
	rent = [1, 2, 3, 4, 5]
	sale = [6, 7, 8, 9]
	# category: -1
	# city: 1 district__city
	# district: -1
	# min_square: square__gte
	# max_square: square__lte
	# min_walls: rooms__gte
	# max_walls: rooms__lte
	# min_floor: floor__gte
	# max_floor: floor__lte
	# min_price: price__gte
	# max_price: price__lte
	# currency: 0
	filters = {k: v for k, v in request.POST.items() if v and v != '-1'}
	if 'currency' in filters:
		if 'min_price' not in filters and 'max_price' not in filters:
			filters.pop('currency')
		else:
			if filters['currency'] == 1:
				if 'min_price' not in filters:
					filters['min_price'] *= 60
				if 'max_price' not in filters:
					filters['max_price'] *= 60
			filters.pop('currency')
	if 'filter' in filters and 'category' in filters:
		filters.pop('category')
	rename_dict_keys(filters, names, commercial, rent, sale)
	posts = Post.objects.filter(is_top=True, verified=True, closed=False, **filters)
	if len(posts) == 0:
		posts = Post.objects.filter(verified=True, closed=False, **filters)[:15]
	return JsonResponse({'status': 'OK', 'html': render_to_string('ajax-posts.html', {'posts': posts})})


def more(request):
	names = {'city': 'district__city', 'min_square': 'square__gte', 'max_square': 'square__lte',
		'min_walls': 'rooms__gte', 'max_walls': 'rooms__lte', 'min_floor': 'floor__gte', 'max_floor': 'floor__lte',
		'min_price': 'price__gte', 'max_price': 'price__lte', }
	commercial = [10, 11, 13]
	rent = [1, 2, 3, 4, 5]
	sale = [6, 7, 8, 9]
	post_ids = list(map(int, request.GET.getlist('post_ids[]', [])))
	filters = {k: v for k, v in request.GET.items() if v and v != '-1' and k != 'post_ids[]'}
	if 'min_price' not in filters and 'max_price' not in filters:
		filters.pop('currency')
	else:
		if filters['currency'] == 1:
			if 'min_price' not in filters:
				filters['min_price'] *= 60
			if 'max_price' not in filters:
				filters['max_price'] *= 60
		filters.pop('currency')
	rename_dict_keys(filters, names, commercial, rent, sale)
	posts = Post.objects.filter(verified=True, closed=False, **filters).exclude(id__in=post_ids).only('id', 'title',
		'currency',
		'price',
		'created',
		'is_top',
		'is_important',
		'category_id',
		'district_id',
		'main_photo_id') \
		.prefetch_related('category', 'district__city', 'main_photo').order_by('-created')[:15]
	return JsonResponse({'status': 'OK', 'posts': post_ids + [item[0] for item in posts.values_list('id')],
		'html': render_to_string('ajax-posts.html', {'posts': posts})})


@login_required
def edit_profile(request):
	if request.method == 'POST':
		data = request.POST
		first_name = data['profile_first_name']
		last_name = data['profile_last_name']
		phone = re.sub("[^\d+]", "", request.POST['profile_phone'])
		user_data = CustomData.objects.get(user_id__exact=request.user.id)
		if first_name != user_data.user.first_name or last_name != user_data.user.last_name or \
				phone != user_data.phone:
			if first_name != user_data.user.first_name:
				user_data.user.first_name = first_name
			if last_name != user_data.user.last_name:
				user_data.user.last_name = last_name
			if phone != user_data.phone:
				user_data.phone = phone
			if user_data.type == 1:
				user_data.verified = False
				user_data.user.is_staff = False
			user_data.user.save()
	return redirect('/')


def edit_post(request):
	if request.method == 'POST':
		data = request.POST
		post_id = data['post_id']

		post = Post.objects.get(id=post_id)

		if request.user.is_staff or post.owner.id == request.user.id:
			title = data['edited_title']
			category = int(data['edited_post_type'])
			price = int(data['edited_estate_price'])
			currency = int(data['edited_estate_currency_value'])
			rooms = int(data['edited_rooms_count'])
			square = float(data['edited_square'])
			floor = int(data['edited_estate_floor'])
			storeys = int(data['edited_estate_storeys'])
			city = int(data['edited_estate_city'])
			district = int(data['edited_estate_district'])
			description = data['edited_description']

			if title != post.title or category != post.category.id or price != post.price or currency != post.currency \
					or rooms != post.rooms or square != post.square or floor != post.floor or storeys != post.storeys \
					or city != post.district.city.id or district != post.district.id or description != post.description:
				if title != post.title:
					post.title = title
				if category != post.category.id:
					post.category_id = category
				if price != post.price:
					post.price = price
				if currency != post.currency:
					post.currency = currency
				if rooms != post.rooms:
					post.rooms = rooms
				if square != post.square:
					post.square = square
				if floor != post.floor:
					post.floor = floor
				if storeys != post.storeys:
					post.storeys = storeys
				if city != post.district.city.id:
					post.district.city_id = city
				if district != post.district.id:
					post.district_id = district
				if description != post.description:
					post.description = description

				post.verified = False
				post.save()

				return redirect('/' + post_id)
		else:
			return JsonResponse({'status': 'error', 'message': 'access denied'})
	else:
		return JsonResponse({'status': 'error', 'message': 'not POST'})


@staff_member_required
def important_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		post.is_important = True
		post.save()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


@staff_member_required
def unimportant_post(request):
	try:
		post = Post.objects.get(pk=request.POST['post_id'])
		post.is_important = False
		post.save()
		return JsonResponse({'status': 'OK', 'message': 'success'})
	except Post.DoesNotExist:
		return JsonResponse({'status': 'error', 'message': 'has no this object'})
	except Exception:
		return JsonResponse({'status': 'error', 'message': 'unknown error'})


def get_top_eight(request):
	# posts = [{'title': post.title}, {'price': post.price} for post in Post.objects.all()[:8]]
	return Response(posts)


class PostList(ListAPIView):  # 28, 29, 31
	queryset = Post.objects.filter(closed=False)
	pagination_class = PostPageNumberPagination
	serializer_class = PostSerializer
	filter_backends = (filters.SearchFilter, DjangoFilterBackend, PostCategoryFilter)  # PostCategoryFilter
	search_fields = ('=id',)# 'title', 'description')  # toDo: ловеркейсить всё
	filter_fields = ('id',
		'price', 'rooms', 'floor', 'storeys', 'total_square', 'living_square', 'kitchen_square', 'corner', 'balcony',
		'loggia', 'district', 'material', 'window', 'state')
	ordering = ('-created',)

	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			new_data = []
			for obj in serializer.data:
				new_obj = obj
				photo_id = obj['main_photo']
				if photo_id:
					new_obj['main_photo'] = request.build_absolute_uri('/')[:-1] + File.objects.get(id=photo_id).url
				new_data.append(new_obj)
			return self.get_paginated_response(new_data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


# permission_classes = (IsAdmin,)

# def get_queryset(self, *args, **kwargs):
# 	queryset_list = Post.objects.all()
# 	# query = self.request.GET.get("q")
# 	# if query:
# 	# 	queryset_list = queryset_list.filter(
# 	# 		Q(id__icontains=query) |
# 	# 		Q(title__icontains=query) |
# 	# 		Q(description__icontains=query)
# 	# 	)
# 	return queryset_list
class PostDetail(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = SinglePostSerializer


class PostUpdate(UpdateAPIView):
	permission_classes = [IsOwnerOrReadOnly]
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class PostDestroy(DestroyAPIView):
	permission_classes = [IsOwnerOrReadOnly]
	queryset = Post.objects.all()
	serializer_class = PostSerializer


class PostCreate(CreateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Post.objects.all()
	serializer_class = PostUpdateSerializer


class CategoryList(ListAPIView):  # 28, 29, 31
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: obj['name'] for obj in serializer.data}
# 	return Response({'results': queryset_list})


class CurrencyList(ListAPIView):  # 28, 29, 31
	queryset = Currency.objects.all()
	serializer_class = CurrencySerializer

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: obj['symbol'] for obj in serializer.data}
# 	return Response({'results': queryset_list})


class StatesList(ListAPIView):
	queryset = State.objects.all()
	serializer_class = StateSerializer

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: obj['name'] for obj in serializer.data}
# 	return Response({'results': queryset_list})


class WindowList(ListAPIView):
	queryset = Window.objects.all()
	serializer_class = WindowSerializer

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: obj['name'] for obj in serializer.data}
# 	return Response({'results': queryset_list})


class MaterialList(ListAPIView):
	queryset = Material.objects.all()
	serializer_class = MaterialSerializer

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: obj['name'] for obj in serializer.data}
# 	return Response({'results': queryset_list})


class UsersList(ListAPIView):
	queryset = CustomData.objects.all()
	serializer_class = UserSerializer

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {
# 		obj['user_id']: {'first_name': obj['first_name'], 'last_name': obj['last_name'], 'phone': obj['phone']} for
# 		obj in
# 		serializer.data}
# 	return Response({'results': queryset_list})


class CitiesList(ListAPIView):
	queryset = City.objects.all()
	serializer_class = CitySerializer

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: obj['name'] for obj in serializer.data}
# 	return Response(queryset_list)


class DistrictsList(ListAPIView):
	queryset = District.objects.all()
	serializer_class = DistrictSerializer
	filter_backends = (DistrictsFilter,)

# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: {'name': obj['name'], 'city': obj['city']} for obj in serializer.data}
# 	return Response(queryset_list)


def recursive_node_to_dict(node):
	result = {
		'id': node.pk,
		'name': node.name,
	}
	children = [recursive_node_to_dict(c) for c in node.get_children()]
	if children:
		result['children'] = children
	return result


class TreeCategoryList(ListAPIView):
	queryset = TreeCategory.objects.all()
	serializer_class = TreeCategorySerializer

	def list(self, request, *args, **kwargs):
		root_nodes = cache_tree_children(self.get_queryset())
		dicts = []
		for n in root_nodes:
			dicts.append(recursive_node_to_dict(n))
		return Response(dicts)


def get_request(request):
	# body_unicode = request.body.decode('utf-8')
	# body = json.loads(body_unicode)
	name = request.POST['name']
	phone = request.POST['phone']
	services = request.POST['services']
	description = request.POST['description']
