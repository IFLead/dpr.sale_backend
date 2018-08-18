import os

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from filer.models import File, Image
from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from url_filter.integrations.drf import DjangoFilterBackend as DjangoUrlFilterBackend

from Main.models import Post, Category, Currency, TreeCategory, State, Window, Material, City, District, CustomData, Client
from Realtor import settings
from .filters import PostCategoryFilter, DistrictsFilter, PostCurrencyFilter, CategoryTreeFilter, CitiesFilter, \
    PostOnlyVisibleFilter, PostAllUsersFilter
from .pagination import PostPageNumberPagination, PostPageAdminPagination
from .permissions import AdminRealtor
from .serializers import AllPostSerializer, PostSerializer, PostUpdateSerializer, CategorySerializer, \
    CurrencySerializer, \
    TreeCategorySerializer, WindowSerializer, MaterialSerializer, StateSerializer, SinglePostSerializer, CitySerializer, \
    DistrictSerializer, UserSerializer, DefaultUserSerializer, PostCreateSerializer, ClientSerializer, ClientUpdateSerializer


class PostList(ListAPIView):
    queryset = Post.objects.filter(closed=False, is_archive=False).prefetch_related(
        'images').order_by('-created')
    pagination_class = PostPageNumberPagination
    serializer_class = PostSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, PostCategoryFilter, DjangoUrlFilterBackend,
                       PostCurrencyFilter, CategoryTreeFilter)  # PostCategoryFilter
    search_fields = ('title', 'description')
    filter_fields = ('id',
                     'price', 'rooms', 'floor', 'storeys', 'total_square', 'living_square', 'kitchen_square',
                     'balcony',
                     'loggia', 'district', 'material', 'window', 'state')
    ordering = ('-created',)


class PostListAll(ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Post.objects.all().prefetch_related('images').order_by('-created')
    pagination_class = PostPageAdminPagination
    serializer_class = AllPostSerializer
    # filter_backends = (filters.SearchFilter, DjangoFilterBackend, PostCategoryFilter, DjangoUrlFilterBackend,
    # PostCurrencyFilter, CategoryTreeFilter)  # PostCategoryFilter
    filter_backends = (filters.OrderingFilter, DjangoUrlFilterBackend,
                       PostOnlyVisibleFilter, PostAllUsersFilter, PostCategoryFilter)
    filter_fields = ('id',)
    # search_fields = ('title', 'description')
    # filter_fields = ('id',
    # 'price', 'rooms', 'floor', 'storeys', 'total_square', 'living_square', 'kitchen_square',
    # 'balcony',
    # 'loggia', 'district', 'material', 'window', 'state')
    ordering_fields = ('id', 'price')

# def list(self, request, *args, **kwargs):
#     queryset = self.filter_queryset(self.get_queryset())
#


#     page = self.paginate_queryset(queryset)
#     if page is not None:
#         serializer = self.get_serializer(page, many=True)
#         new_data = []
#         for obj in serializer.data:
#             new_obj = obj
#             photo_id = obj['main_photo']
#             if photo_id:
#                 new_obj['main_photo'] = Image.objects.get(id=photo_id).url
#             new_data.append(new_obj)
#         return self.get_paginated_response(new_data)
#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)


def get_queryset(self, *args, **kwargs):
    queryset_list = Post.objects.all()
    query = self.request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(id__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    return queryset_list


class PostDetail(APIView):
    queryset = Post.objects.all().prefetch_related('images')
    serializer_class = PostUpdateSerializer

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        posts_data = self.get_object(pk)
        serializer = PostUpdateSerializer(posts_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        posts_data = self.get_object(pk)
        serializer = PostUpdateSerializer(
            posts_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        posts_data = self.get_object(pk)
        posts_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PostUpdate(UpdateAPIView):
# 	# permission_classes = IsOwnerOrReadOnly
# 	queryset = Post.objects.all()
# 	serializer_class = PostUpdateSerializer


class PostDestroy(DestroyAPIView):
    # permission_classes = IsOwnerOrReadOnly
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostAll(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer


class UserCreate(CreateAPIView):
    permission_classes = AdminRealtor
    queryset = User.objects.all()
    serializer_class = DefaultUserSerializer


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
    filter_backends = (CitiesFilter,)


# def list(self, request, *args, **kwargs):
# 	queryset = self.filter_queryset(self.get_queryset())
# 	serializer = self.get_serializer(queryset, many=True)
# 	queryset_list = {obj['id']: obj['name'] for obj in serializer.data}
# 	return Response(queryset_list)


class DistrictsList(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = (DistrictsFilter,)


class ClientList(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetail(APIView):
    queryset = Client.objects.all()
    serializer_class = ClientUpdateSerializer

    def get_object(self, pk):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cleint_data = self.get_object(pk)
        serializer = ClientUpdateSerializer(cleint_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cleint_data = self.get_object(pk)
        serializer = ClientUpdateSerializer(
            cleint_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cleint_data = self.get_object(pk)
        cleint_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        m = Image()
        m.image_file = file_obj
        # m.product = obj
        m.save()
        return JsonResponse({'status': 'OK', 'id': m.id, 'url': m.url})


@csrf_exempt
@api_view(['POST'])
def get_request(request):
    name = request.data['name']
    phone = request.data['phone']
    services = request.data['services']
    description = request.data['description']
    text = """Имя: {0}
    Номер телефона: {1}
    Тип услуги: {2}
    Текст: {3}""".format(name, phone, services, description)
    send_mail(
        'Заявка с сайта',
        text,
        settings.EMAIL_HOST_USER,
        ['igos.321@gmail.com', 'info@dpr.sale'],
        fail_silently=False,
    )
    return JsonResponse({'status': 'OK'})


@csrf_exempt
def get_photoes(request):
    file = request.FILES['file']
    name = file.name
    path = default_storage.save(name, ContentFile(file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    image = Image.objects.create(original_filename=name,
                                 file=tmp_file)
    MiniImage.objects.create(name=name, main_photo=image)

    return JsonResponse({'status': 'OK'})
