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
    Image = models.ImageField(upload_to='images/')
    Starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    Seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Listings")
    Category = models.CharField(choices=CATEGORIES, max_length=100)

class Bids(models.Model):
    Item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="Bids")
    Bid = models.DecimalField(max_digits=10, decimal_places=2)
    Bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    Time_bid = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    Item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="Comments")
    Comment = models.TextField()
    Time_commented = models.DateTimeField(auto_now_add=True)

class ActiveItems(models.Model):
    Item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="ActiveItems")
    Current_Price = models.DecimalField(max_digits=10, decimal_places=2)
    Date_uploaded = models.DateTimeField(auto_now_add=True)

class InactiveItems(models.Model):
    Item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="InactiveItems")
    Sold_on = models.DateTimeField(auto_now_add=True)

