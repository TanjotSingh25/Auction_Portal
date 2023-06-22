from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Items(models.Model):
    CATEGORIES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('collectibles', 'Collectibles')
    ]

    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Image = models.ImageField()
    Starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    Seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    Category = models.CharField(choices=CATEGORIES, max_length=100)

class Bids(models.Model):
    item = models.ManyToManyField(Items, related_name="Bids")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ManyToManyField(User, related_name="Bidder")
    time_bid = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    item = models.ManyToManyField(Items, related_name="Comments")
    comment = models.TextField()
    time_commented = models.DateTimeField(auto_now_add=True)

class ActiveItems(models.Model):
    item = models.ManyToManyField(Items, related_name="ActiveItems")
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_uploaded = models.DateTimeField(auto_now_add=True)

class InactiveItems(models.Model):
    item = models.ManyToManyField(Items, related_name="InactiveItems")
    sold_on = models.DateTimeField(auto_now_add=True)

