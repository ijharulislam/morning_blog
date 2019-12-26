import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from ..models import Author


class AuthorFields():
    name = graphene.String()
    description = graphene.String()
 

class AuthorType(DjangoObjectType, AuthorFields):
    class Meta:
        model = Author

    id = graphene.ID(required=True)

class AuthorInputType(graphene.InputObjectType, AuthorFields):
    id = graphene.ID()


class DeleteAuthorInputType(graphene.InputObjectType):
     id = graphene.ID(required=True)


class Query(ObjectType):
    author = graphene.Field(AuthorType, id=graphene.ID(required=True))
    authors = graphene.List(AuthorType)

    def resolve_author(self, info, **kwargs):
        id = kwargs.get("id")
        return Author.objects.get(id=id)

    def resolve_authors(self, info, **kwargs):
        return Author.objects.all()


class CreateAuthor(graphene.Mutation):
    class Arguments:
        input = AuthorInputType(required=True)

    ok = graphene.Boolean()
    author = graphene.Field(AuthorType)
    
    @staticmethod
    def mutate(root, info, input):
        author = Author()
        for key, val in input.items():
            setattr(author, key, val)
        author.save()
        return CreateAuthor(ok=True, author=author)


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        input = AuthorInputType(required=True)

    ok = graphene.Boolean()
    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, input):
        id = input.get("id")
        author = Author.objects.get(id=id)
        for key, val in input.items():
            setattr(author, key, val)
        author.save()
        return CreateAuthor(ok=True, author=author)


class DeleteAuthor(graphene.Mutation):
    class Arguments:
        input = DeleteAuthorInputType()

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input):
        id = input.get("id")
        author = Author.objects.get(id=id)
        author.delete()
        return DeleteAuthor(ok=True)


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)