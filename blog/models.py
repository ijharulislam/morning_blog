from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField() 


class Blog(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()  


class BlogTag(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_tags")
    tag = models.CharField(max_length=250) 