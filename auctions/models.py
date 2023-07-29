from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=850, default='')
    image = models.ImageField(upload_to='auctions/uploads/')
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"""Title: {self.title}, Description: {self.description}, poster: {self.poster}"""

class Bids(models.Model):
    amount = models.IntegerField()
    listing = models.ForeignKey(Listing,null=True, on_delete=models.SET_NULL)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    saying = models.CharField(max_length=300)
    listing = models.ForeignKey(Listing, null=True, on_delete=models.SET_NULL)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)