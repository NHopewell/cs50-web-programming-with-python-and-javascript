from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Watchlist, Bid, ClosedAuctions, CATEGORY_CHOICES
from .forms import NewListingForm
from .helpers import (
    get_listings_by_category, all_categories, map_category, get_diff_days
)


def index(request):
    listings = Listing.objects.filter(status='active')
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def closed_listings(request):
    listings = Listing.objects.filter(status='closed')
    return render(request, "auctions/closed_listings.html", {
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

    listing = Listing.objects.get(pk=listing_id)
    owner = User.objects.get(pk=listing.owner_id)
    category = map_category(listing.category)
    days_active = get_diff_days(listing.date_posted)

    bids = Bid.objects.filter(listing_id=listing.id)
    all_bids = None
    if bids:
        all_bids = [q.bid for q in Bid.objects.filter(listing_id=listing.id)]
        top_bid = format(float(max(all_bids)), '.2f')
        top_bidder = User.objects.get(pk=Bid.objects.get(bid=top_bid).bidder_id).username
    else:
        top_bid = None
        top_bidder = None
    
    if request.method == 'POST' and 'submit-watchlist' in request.POST:
        already_on_watchlist = Watchlist.objects.filter(listing_id=listing_id, user_id=request.user.id)
        if not already_on_watchlist:
            watchlist_item = Watchlist(listing_id=listing_id, user_id=request.user.id)
            watchlist_item.save()

            messages.info(request, 'Added to watchlist.')

            return HttpResponseRedirect(reverse("watchlist"))
        else:
            Watchlist.objects.filter(listing_id=listing_id, user_id=request.user.id).delete()

            messages.info(request, 'Removed from watchlist.')

            return render(request, "auctions/listing.html", {
                "listing": listing,
                "owner": owner,
                "category": category,
                "days_active": days_active,
                "top_bid": top_bid,
                "top_bidder": top_bidder,
                "on_watchlist": False
            })
    elif request.method == 'POST' and 'submit-bid' in request.POST:
        bid = float(request.POST['bid'])
        
        if (bid > listing.starting_bid):
            if not all_bids or (bid > float(top_bid)):
                new_bid = Bid(bid=bid, bidder_id=request.user.id, listing_id=listing.id)
                new_bid.save()
                top_bid = new_bid.bid
                top_bidder = request.user.username

                messages.success(request, 'Your bid has been submitted')

                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "owner": owner,
                    "category": category,
                    "days_active": days_active,
                    "top_bid": top_bid,
                    "top_bidder": top_bidder,
                    "on_watchlist": False
                })
            else:
                messages.error(request, 'You cannot bid less than the current highest bidder. Your bid was not submitted.')

                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "owner": owner,
                    "category": category,
                    "days_active": days_active,
                    "top_bid": top_bid,
                    "top_bidder": top_bidder,
                    "on_watchlist": False
                })

        else:
            messages.error(request, 'You must bid more than the starting bid. Your bid was not submitted.')
            
            return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "owner": owner,
                    "category": category,
                    "days_active": days_active,
                    "top_bid": top_bid,
                    "top_bidder": top_bidder,
                    "on_watchlist": False
                })
    else:
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
            "top_bid": top_bid,
            "top_bidder": top_bidder,
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
def close_listing(request, listing_id, top_bidder):

    if request.method == "POST":
        listing = Listing.objects.filter(pk=listing_id)
        listing.update(status="closed")
        winner = User.objects.get(username=top_bidder)
        closed_auction = ClosedAuctions(listing_id=listing_id, winner=winner)
        closed_auction.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        listing = Listing.objects.get(pk=listing_id)

        return render(request, "auctions/close_listing.html", {
            "listing": listing,
            "top_bidder": top_bidder
            })
    

@login_required
def my_listings(request):

    listings = Listing.objects.filter(owner_id=request.user.id)

    return render(request, "auctions/my-listings.html", {
        "listings": listings
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