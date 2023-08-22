from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,AuctionListing,Comment,Bid,Category


def index(request):
    if request.method =="GET":
        
        list_auction = AuctionListing.objects.filter(disponible=True)
        all_category= Category.objects.all()
        return render(request, "auctions/index.html",{
            "auction": list_auction,
            "category": all_category
        })
    else:
        return render(request, "auctions/index.html")


def category(request):
    if request.method == "POST":
        category_form = request.POST["category_"]
        category_filter = Category.objects.get(This_category=category_form)
        list_auction = AuctionListing.objects.filter(disponible=True,category=category_filter)
        all_category = Category.objects.all()
        return render(request, "auctions/index.html",{
            "auction": list_auction,
            "category": all_category
        })
    else:
        return render(request, "auctions/category.html")
       

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def new_auction(request):
    if request.method =="GET":
        all_category=Category.objects.all()
        return render(request, "auctions/new_auction.html",{
            "category": all_category
        })
    else:
#Buscando la info que se ha ingresado via post
        title= request.POST["title"]
        description= request.POST["content"]
        bid= request.POST["price"]
        category=request.POST["category"]
        image=request.POST["image"]
        #preguntando que usuario creo esto en este caso sera el que este conectado
        actual_user=request.user
        #obteniendo la categoria
        all_category= Category.objects.get(This_category=category)
         
        
        new_bid=Bid(
            bid=float(bid),
            users=actual_user
        )
        new_bid.save()

        
        #Creando una nueva lista desde el formulario
        create_listing= AuctionListing(
            item=title,
            description=description,
            price=new_bid,
            category=all_category,
            image=image,
            users=actual_user
        )
        create_listing.save()
    return HttpResponseRedirect(reverse("index"))

def listing(request,id):
    if request.method == "GET":
        listing_data = AuctionListing.objects.get(pk=id)
        watch_list=request.user in listing_data.watchlist.all()
        all_comment= Comment.objects.filter(actual_listing=listing_data)
        owner = request.user.username == listing_data.users.username
        return render(request, "auctions/listing.html",{
            "listing":listing_data,
            "watch_list":watch_list,
            "comment":all_comment,
            "owner" : owner
        })

def close_auction(request,id):
    listing_data= AuctionListing.objects.get(pk=id)
    actual_user=request.user.username
    listing_data.disponible = False
    listing_data.save()
    owner = request.user.username == listing_data.users.username
    watch_list=request.user in listing_data.watchlist.all()
    all_comment= Comment.objects.filter(actual_listing=listing_data)
    return render(request,"auctions/listing.html",{
        "message":"Congratulations your auction is close",
        "listing":listing_data,
        "watch_list":watch_list,
        "comment":all_comment,
        "owner" : owner,
        "update": True
    })

def bid(request,id):
    if request.method =="POST":
        create_bid = request.POST["bid"]
        listing_data = AuctionListing.objects.get(pk=id)
        watch_list=request.user in listing_data.watchlist.all()
        all_comment= Comment.objects.filter(actual_listing=listing_data)
        owner = request.user.username == listing_data.users.user
        if int(create_bid) > listing_data.price.bid:
            new_bid=Bid( bid=int(create_bid), users=request.user)
            new_bid.save()
            listing_data.price=new_bid
            listing_data.save()
            return render(request,"auctions/listing.html",{
                "listing": listing_data,
                "message": "Bid was updated succesfully",
                "update": True,
                "watch_list":watch_list,
                "comment":all_comment,
                "owner" : owner
            })
        else:
            return render(request,"auctions/listing.html",{
                    "listing": listing_data,
                    "message": "The Bid cant be created",
                    "update": False,
                    "watch_list":watch_list,
                    "comment":all_comment,
                    "owner" : owner

            })
def watchlist(request):
    current_user = request.user
    listing_data= current_user.user_watclist.all()
    return render(request, "auctions/watchlist.html",{
        "auction":listing_data
    })



    
def addwatchlist(request, id):
    listing_data= AuctionListing.objects.get(pk=id)
    actual_user=request.user
    listing_data.watchlist.add(actual_user)
    return HttpResponseRedirect(reverse("listing",args=(id, )))


def removewatchlist(request, id):
    listing_data= AuctionListing.objects.get(pk=id)
    actual_user=request.user
    listing_data.watchlist.remove(actual_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def comment(request, id):
    actual_user=request.user
    listing_data= AuctionListing.objects.get(pk=id)
    comment= request.POST["comment"]
    new_comment= Comment(
        comment=comment,
        author= actual_user,
        actual_listing=listing_data
    )
    new_comment.save()
    
    return HttpResponseRedirect(reverse("listing", args=(id, )))








        
