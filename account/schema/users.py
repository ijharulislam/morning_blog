import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType, ObjectType

from account.models import User, Role, Right
from blog.utils import can 


class UserFields:
    id = graphene.ID()
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)


class RightFields:
    id = graphene.ID()
    name = graphene.String()
    codename = graphene.String()
    description = graphene.String()


class RoleFiels:
    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    

class RightType(DjangoObjectType, RightFields):
    class Meta:
        model = Right


class RoleType(DjangoObjectType, RoleFiels):
    class Meta:
        model = Role

    rights = graphene.List(RightType)


class UserType(DjangoObjectType, UserFields):
    class Meta:
        model = User


class RightInputType(graphene.InputObjectType, RightFields):
    pass


class RoleInputType(graphene.InputObjectType, RoleFiels):
    rights = graphene.List(RightInputType)


class UserInputType(graphene.InputObjectType, UserFields):
    role = graphene.Field(RoleInputType)


class Query(ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    @can("manage_own_profile")
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
        rights = input.role.rights
        right_ids = []
        for right in rights:
            obj, created = Right.objects.get_or_create(name=right.name, codename=right.codename)
            right_ids.append(obj.id)
        role, created = Role.objects.get_or_create(name=input.role.name, description=input.role.description)
        role.rights.set(right_ids)

        user = User()
        for key, val in input.items():
            if key is "role":
                val = role
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
