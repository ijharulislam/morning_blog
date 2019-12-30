import graphene
from graphene_django.types import DjangoObjectType, ObjectType

from .authors import AuthorType
from ..models import Blog
from ..forms import CreateBlogForm
from .blog_tags import BlogTagType, BlogTagInputType


class BlogFields():
    title = graphene.String()
    body = graphene.String()


class BlogType(DjangoObjectType, BlogFields):
    class Meta:
        model = Blog

    id = graphene.ID(required=True)
    author = AuthorType()
    blog_tags = BlogTagType()


class BlogInputType(graphene.InputObjectType, BlogFields):
    id = graphene.ID()
    author_id = graphene.ID()
    tags = graphene.List(BlogTagInputType)
    deleted_tags = graphene.List(BlogTagInputType)


class DeleteBlogInputType(graphene.InputObjectType):
     id = graphene.ID(required=True)


class BlogErrorsInputType(graphene.ObjectType, BlogFields):
     id = graphene.String()
     author_id = graphene.String()


class Query(ObjectType):
    blog = graphene.Field(BlogType, id=graphene.ID(required=True))
    blogs = graphene.List(BlogType)
    
    def resolve_blog(self, info, **kwargs):
        id = kwargs.get("id")
        return Blog.objects.get(id=id)

    def resolve_blogs(self, info, **kwargs):
        return Blog.objects.all()


class CreateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInputType(required=True)

    ok = graphene.Boolean()
    blog = graphene.Field(BlogType)
    errors = graphene.Field(BlogErrorsInputType)

    @staticmethod
    def mutate(root, info, input):
        form = CreateBlogForm(data=input)
        if form.is_valid():
            blog = form.save()
            return CreateBlog(ok=True, blog=blog, errors=form.errors)
        return CreateBlog(ok=False, errors=form.errors)


class UpdateBlog(graphene.Mutation):
    class Arguments:
        input = BlogInputType(required=True)

    ok = graphene.Boolean()
    blog = graphene.Field(BlogType)

    @staticmethod
    def mutate(root, info, input):
        id = input.get("id")
        blog = Blog.objects.get(id=id)
        for key, val in input.items():
            setattr(blog, key, val)
        blog.save()
        return UpdateBlog(ok=True, blog=blog)


class DeleteBlog(graphene.Mutation):
    class Arguments:
        input = DeleteBlogInputType(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input):
        id = input.get("id")
        blog = Blog.objects.get(id=id)
        blog.delete()
        return DeleteBlog(ok=True)


class Mutation(graphene.ObjectType):
    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()
    delete_blog = DeleteBlog.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)