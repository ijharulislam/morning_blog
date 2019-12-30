import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from ..models import BlogTag


class BlogTagFields():
    blog_id = graphene.ID()
    tag = graphene.String()
    id = graphene.ID()


class BlogTagType(DjangoObjectType, BlogTagFields):
    class Meta:
        model = BlogTag

    
class BlogTagInputType(graphene.InputObjectType, BlogTagFields):
    pass