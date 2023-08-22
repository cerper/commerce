from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
   first_name= models.CharField(max_length=64)
   email= models.EmailField()
   
class Category(models.Model):
    This_category = models.CharField(max_length=500 )
    def __str__(self):
        return self.This_category
class Bid(models.Model):
    bid = models.FloatField()
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    def __str__(self):
        return f"initial bid: {self.bid} "
class AuctionListing(models.Model):
    item =  models.CharField(max_length=70)
    description = models.CharField(max_length=500 )
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    image= models.CharField(max_length=3000)
    price= models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="actual_bid")
    disponible= models.BooleanField(default= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    watchlist = models.ManyToManyField(User,blank=True,null=True, related_name="user_watclist")
    bid = models.ManyToManyField(User, blank=True,null=True, related_name="user_bid")
   
    def __str__(self):
        return f"Item:{self.item}, Description:{self.description}, Image:{self.image} Price:{self.price} "


    
class Comment(models.Model):
    comment= models.CharField(max_length=500)
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    actual_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE,null=True, related_name="actual_listing") 
    def __str__(self):
        return f"author: {self.author} comment in this: {self.comment} "