from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
from .models import User

def index(request):
    if request.method == "POST":
        category_selected = request.POST["category"]
        if category_selected.lower() == "categories":
            categories = [("Categories", "selected")]
            for category in Items.CATEGORIES:
                categories.append((category[1], ""))
            return render(request, "auctions/index.html", {
                "Items" : ActiveItems.objects.all(),
                "categories" : categories
            })
        items = ActiveItems.objects.all()
        category_to_display = []
        for i in range(len(items)):
            item_category = items[i].Item.Category
            if item_category.lower() == category_selected.lower():
                category_to_display.append(items[i])
        categories = [("Categories", "")]
        for category in Items.CATEGORIES:
            if category[1].lower() == category_selected.lower():
                categories.append((category[1], "selected"))
            else:
                categories.append((category[1], ""))
        return render(request, "auctions/index.html", {
            "Items" : category_to_display,
            "categories" : categories
        })
    else:
        message = ''
        if 'message' in request.GET:
            message = request.GET.get('message')
        categories = [("Categories", "selected")]
        for category in Items.CATEGORIES:
            categories.append((category[1], ""))
        return render(request, "auctions/index.html", {
            "Message" : message,
            "Items" : ActiveItems.objects.all(),
            "categories_navigation" : categories
        })


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


def createListings(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.FILES.get("image")
        startingPrice = float(request.POST["startingPrice"])
        category = request.POST["category"].strip().lower()
        user = request.user
        user = User.objects.get(username=user)

        if not title or not description or not image or not startingPrice or not category:
            message = "Error Creating Listing: Details Missing"
        elif not (isinstance(title, str) and isinstance(description, str) and isinstance(startingPrice, float)):
            message = "Error Creating Listing: Illegal Details Submitted"
        else:
            listing = Items(Title=title, Description=description, Image=image, Starting_price=startingPrice, Seller=user, Category=category)
            listing.save()
            listing = Items.objects.get(Item_id=listing.Item_id)
            active = ActiveItems(Item=listing, Highiest_Bid=startingPrice)
            active.save()
            message = "Listing Successfully Added"
        return HttpResponseRedirect(reverse("index") + '?message=' + message)
    else:
        categories = []
        for category in Items.CATEGORIES:
            categories.append(category[1])
        return render(request, "auctions/createlisting.html", {
            "categories" : categories,
            "users" : User.objects.all()
        })
    

def openListing(request, listing_id):
    print(request)
    if request.method == "POST":
        bid = request.POST["bid"]
        if not bid:
            message = "Error Bidding: Amount Missing"
        else:
            try:
                bid = float(bid)
            except:
                message = "Error Bidding: Amount is of wrong format"
            else:
                user = request.user
                user = User.objects.get(username=user)
                activeItem = ActiveItems.objects.get(Item=Items.objects.get(Item_id=int(listing_id)))
                if activeItem.Highiest_Bid >= bid:
                    message = "Your bid cannot be less or equal than the Current Highiest Bid."
                else:
                    activeItem.Highiest_Bid = bid
                    activeItem.save()
                    bidder = Bids(Item=activeItem.Item, Bid=bid, Bidder=user)
                    bidder.save()
                    watchlist_item = WatchList(Item=activeItem.Item, User=user)
                    watchlist_item.save()
                    message = "Your bid has successfully been registered."
        return HttpResponseRedirect(reverse("index") + '?message=' + message)
    else:
        owner = False
        listing_info = ActiveItems.objects.get(Item=Items.objects.get(Item_id=listing_id))
        user = request.user
        current_user = User.objects.get(username=user)
        notOnWatch = True
        if WatchList.objects.filter(Item=listing_info.Item, User=current_user).exists():
            notOnWatch = False
        if listing_info.Item.Seller == current_user:
            print("Yes")
            owner = True
        bids_count = len(listing_info.Item.Bids.all())
        return render(request, "auctions/listing.html", {
            "listing" : listing_info,
            "bids_count" : bids_count,
            "owner" : owner,
            "notOnWatch" : notOnWatch
        })
    

def closeListing(request):
    if request.method == "POST":
        id = int(request.POST["id"])
        item = ActiveItems.objects.get(Item=Items.objects.get(Item_id=id))
        inactiveItem = InactiveItems(Item=item.Item, Final_Price=item.Highiest_Bid)
        inactiveItem.save()
        item.delete()
        message = "Listing Successfully Closed"
    return HttpResponseRedirect(reverse("index") + '?message=' + message)


def addToWatchList(request, listing_id):
    item = Items.objects.get(Item_id=int(listing_id))
    user = request.user
    user = User.objects.get(username=user)
    if not WatchList.objects.filter(Item=item, User=user).exists():
        watchlist_item = WatchList(Item=item, User=user)
        watchlist_item.save()
    return HttpResponseRedirect(reverse("openListing", args=[listing_id]))


def watchlist(request):
    user = request.user
    user = User.objects.get(username=user)
    watchlist_items = WatchList.objects.filter(User=user)
    Items = []
    for item in watchlist_items:
        if ActiveItems.objects.filter(Item=item.Item).exists():
            tuple = (ActiveItems.objects.get(Item=item.Item), True, "")
            Items.append(tuple)
        else:
            tuple = (InactiveItems.objects.get(Item=item.Item), False, 'style=pointer-events:none;')
            Items.append(tuple)
    return render(request, "auctions/watchlist.html", {
        "Items" : Items
    })