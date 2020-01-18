from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        db_table = "user"

    username = models.CharField(
        max_length=64,
        unique=True
    )
    role = models.ForeignKey(
        'account.Role', 
        on_delete=models.CASCADE, 
        blank=True, null=True
    )

    def __str__(self):
        return self.username


class Right(models.Model):

    class Meta:
        db_table = "right"
        ordering = ["name"]

    name = models.CharField(max_length=64)
    codename = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Role(models.Model):

    class Meta:
        db_table = "role"

    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    rights = models.ManyToManyField(Right)

    def __str__(self):
        return self.name

