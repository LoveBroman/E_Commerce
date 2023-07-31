from django.contrib.auth.models import AbstractUser
from django.db import models
from time import time


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=850, default='')
    image = models.ImageField(upload_to='auctions/uploads/')
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    def __str__(self):
        return f"""Title: {self.title}, Description: {self.description}, poster: {self.poster}"""

class Bid(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing, null=True, on_delete=models.SET_NULL)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    saying = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.SET_NULL)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)