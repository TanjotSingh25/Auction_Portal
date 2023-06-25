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
            "categories" : categories
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
            listing = Items.objects.get(id=listing.id)
            active = ActiveItems(Item=listing, Current_Price=startingPrice)
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
    
def openListing(request, listing):
    return render(request, "auctions/listing.html")