from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField() 


class Blog(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    body = models.TextField()  