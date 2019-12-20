import graphene
from blog.schema.authors import schema as author_schema
from blog.schema.blogs import schema as blog_schema


class Query(author_schema.Query, blog_schema.Query):
    pass


class Mutation(author_schema.Mutation, blog_schema.Mutation):
    pass
    
schema = graphene.Schema(query=Query, mutation=Mutation)
