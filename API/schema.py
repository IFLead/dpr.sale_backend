import graphene
from graphene import InputObjectType
from graphene.relay import ClientIDMutation
from graphene_django import DjangoObjectType
from Main.models import District, City


class CityType(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = ['name']


class DistrictType(DjangoObjectType):
    class Meta:
        model = District
        filter_fields = ['name']


class DistrictCreateInput(InputObjectType):
    name = graphene.String(required=True)


class CityCreateInput(InputObjectType):
    name = graphene.String(required=True)


class CreateCity(ClientIDMutation):
    class Input:
        # CityCreateInput class used as argument here.
        city = graphene.Argument(CityCreateInput)

    new_city = graphene.Field(CityType)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        city_data = args.get('city')  # get the City input from the args
        city = City()  # get an instance of the City model here
        new_city = update_create_instance(city, city_data)  # use custom function to create City

        return cls(new_city=new_city)  # newly created City instance returned.


class UpdateCity(ClientIDMutation):
    class Input:
        city = graphene.Argument(CityCreateInput)  # get the City input from the args
        name = graphene.String(required=True)  # get the City name

    errors = graphene.List(graphene.String)
    updated_city = graphene.Field(CityType)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):

        try:
            city_instance = get_object(City, args['name'])  # get City by name
            if city_instance:
                # modify and update City model instance
                city_data = args.get('city')
                updated_city = update_create_instance(city_instance, city_data)
                return cls(updated_city=updated_city)
        except ValidationError as e:
            # return an error if something wrong happens
            return cls(updated_city=None, errors=get_errors(e))


class Query(object):
    all_cities = graphene.List(CityType)
    city = graphene.Field(CityType,
        id=graphene.Int(),
        name=graphene.String())
    all_disctricts = graphene.List(DistrictType)
    district = graphene.Field(DistrictType,
        id=graphene.Int(),
        name=graphene.String())

    def resolve_all_districts(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return District.select_related('cities').all()

    def resolve_all_cities(self, info, **kwargs):
        return City.objects.all()

    def resolve_district(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return District.objects.get(pk=id)

        if name is not None:
            return District.objects.get(name=name)

        return None

    def resolve_city(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return City.objects.get(pk=id)

        if name is not None:
            return City.objects.get(name=name)

        return None
