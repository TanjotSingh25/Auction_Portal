from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

class Items(models.Model):
    CATEGORIES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('collectibles', 'Collectibles')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    starting_price = models.DecimalField()
    current_price = models.DecimalField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    category = models.CharField(choices=CATEGORIES)

class Bids(models.Model):
    item = models.ForeignObject(Items, on_delete=models.CASCADE, related_name="Bids")
    bid = models.DecimalField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bidder")
    time_bid = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    item = models.ForeignObject(Items, on_delete=models.CASCADE, related_name="Comments")
    comment = models.TextField()
    time_commented = models.DateTimeField(auto_now_add=True)

class ActiveItems(models.Model):
    item = models.ForeignObject(Items, on_delete=models.CASCADE, related_name="ActiveItems")
    date_uploaded = models.DateTimeField(auto_now_add=True)

class InactiveItems(models.Model):
    item = models.ForeignObject(Items, on_delete=models.CASCADE, related_name="Inactive Items")
    sold_on = models.DateTimeField(auto_now_add=True)