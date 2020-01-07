import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType, ObjectType

from django.contrib.auth import get_user_model


User = get_user_model()


class UserFields:
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)


class UserType(DjangoObjectType, UserFields):
    class Meta:
        model = User


class UserInputType(graphene.InputObjectType, UserFields):
    id = graphene.ID()


class Query(ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Please login!')
        return user

    def resolve_users(self, info, **kwargs):
        return User.objects.all()    


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInputType(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)
    
    @staticmethod
    def mutate(root, info, input):
        user = User()
        for key, val in input.items():
            setattr(user, key, val)
        user.set_password(input.password)    
        user.save()
        return CreateUser(ok=True, user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
