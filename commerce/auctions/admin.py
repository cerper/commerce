from django.contrib import admin
from .models import AuctionListing,Category,Bid,Comment,User
# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
