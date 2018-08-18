import graphene
import API.schema


class Mutation(graphene.ObjectType):
    create_or_update_city = API.schema.CityCreateUpdateMutation.Field()  # CityCreateUpdateMutationInput


class Query(API.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
