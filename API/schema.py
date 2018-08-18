import graphene
from graphene_django import DjangoObjectType
from django.core.exceptions import ValidationError
from Main.models import City, District
from graphene_django.rest_framework.mutation import SerializerMutation
from .serializers import CitySerializer
from django.db.models import Q
from graphene_django.filter import DjangoFilterConnectionField


class CityNode(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = {
            'name': ['exact', 'istartswith'],
            'id': ['exact'],
        }
        interfaces = (graphene.relay.Node,)


class DistrictNode(DjangoObjectType):
    class Meta:
        model = District
        filter_fields = ['name']
        interfaces = (graphene.relay.Node,)


class CityType(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = ['id', 'name']


class DistrictType(DjangoObjectType):
    class Meta:
        model = District


class Query(graphene.ObjectType):
    city = graphene.Field(CityType,
        id=graphene.Int(),
        name=graphene.String())
    all_cities = graphene.List(
        CityType,
        id=graphene.Int(),
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int(),
    )
    district = graphene.Field(DistrictType,
        id=graphene.Int(),
        name=graphene.String())
    all_districts = graphene.List(DistrictType)

    node_cities = graphene.relay.Node.Field(CityNode)
    node_districts = graphene.relay.Node.Field(DistrictNode)


    def resolve_all_cities(self, info, search=None, first=None, skip=None, **kwargs):
        qs = City.objects.all()

        if search:
            filter = (
                Q(name__icontains=search) |
                Q(id__gt=search)
            )
            qs = qs.filter(filter)

        if skip:
            qs = qs[skip::]

        if first:
            qs = qs[:first]

        return qs

    def resolve_all_districts(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return District.objects.all()

    def resolve_city(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return City.objects.get(pk=id)

        if name is not None:
            return City.objects.get(name=name)

        return None

    def resolve_district(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return District.objects.get(pk=id)

        if name is not None:
            return District.objects.get(name=name)

        return None


class CityCreateUpdateMutation(SerializerMutation):
    class Meta:
        serializer_class = CitySerializer
        model_operations = ['update', 'create']
        lookup_field = 'id'
