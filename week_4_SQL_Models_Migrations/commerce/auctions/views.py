from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist, CATEGORY_CHOICES
from .forms import NewListingForm
from .helpers import (
    get_listings_by_category, all_categories, map_category, get_diff_days
)


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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


def listing(request, listing_id):
    
    if request.method == 'POST' and 'submit-watchlist' in request.POST:
        already_on_watchlist = Watchlist.objects.filter(listing_id=listing_id, user_id=request.user.id)
        if not already_on_watchlist:
            watchlist_item = Watchlist(listing_id=listing_id, user_id=request.user.id)
            watchlist_item.save()

            messages.success(request, 'Added to watchlist.')

            return HttpResponseRedirect(reverse("watchlist"))
        else:
            Watchlist.objects.filter(listing_id=listing_id, user_id=request.user.id).delete()
            listing = Listing.objects.get(pk=listing_id)
            owner = User.objects.get(pk=listing.owner_id)
            category = map_category(listing.category)
            days_active = get_diff_days(listing.date_posted)

            messages.success(request, 'Removed from watchlist.')

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "owner": owner,
                "category": category,
                "days_active": days_active,
                "on_watchlist": False
            })
    elif request.method == 'POST' and 'submit-bid' in request.POST:
        pass
    else:
        listing = Listing.objects.get(pk=listing_id)
        owner = User.objects.get(pk=listing.owner_id)
        category = map_category(listing.category)
        days_active = get_diff_days(listing.date_posted)
        watchlist = Watchlist.objects.filter(listing_id=listing_id, user_id=request.user.id)

        if watchlist:
            on_watchlist = True
        else:
            on_watchlist = False

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "owner": owner,
            "category": category,
            "days_active": days_active,
            "on_watchlist": on_watchlist
        })


@login_required
def create_listing(request):

    if request.method == 'POST':
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()

            return HttpResponseRedirect(reverse("index"))
    else:
            
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm()
        })


@login_required
def delete_listing(request, listing_id):

    if request.method == "POST":
        Listing.objects.filter(pk=listing_id).delete()

        return HttpResponseRedirect(reverse("index"))
    else:
        listing = Listing.objects.get(pk=listing_id)
    
        return render(request, "auctions/delete_listing.html", {
            "listing": listing
        })


@login_required
def watchlist(request):

    rows = Watchlist.objects.filter(user_id=request.user.id)
    watchlist = []
    for row in rows:
        watchlist.append(Listing.objects.get(pk=row.listing_id))


    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


def categories(request):

    categories = all_categories(Listing)
    
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):

    category, listings = get_listings_by_category(Listing, category)

    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })




