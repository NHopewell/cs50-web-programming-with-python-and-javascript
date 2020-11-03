import datetime
from math import modf

from .models import User, Listing, Watchlist, CATEGORY_CHOICES

def silver_and_gold(bid):
    """given a float, return fractional part as silver, rest as gold"""
    s, g = modf(bid)
    return (int(s*100), int(g))

def get_diff_days(date):
    """return diff between two datetimes as days"""
    date_format = "%Y-%m-%d"
    date_one = datetime.datetime.strptime(str(date).split()[0], date_format)
    date_two = datetime.datetime.strptime(str(datetime.date.today()), date_format)

    delta_days = (date_two - date_one).days

    return delta_days


def map_category(category, choices=CATEGORY_CHOICES):
    """map key to category val"""
    for (k,v) in choices:
        if k == category:
            return v

def all_categories(Listing):
    """map categories to associated listings as dict"""
    all_categories = ['Art & Collectibles', 'Clothing', 
        'Electronics', 'Health & Beauty', 'Home & Yard', 
        'Jewellery', 'Sporting Goods']
    category_listings = [Listing.objects.filter(category=cat) for cat in all_categories]

    return dict(zip(all_categories, category_listings))


def get_listings_by_category(Listing, category, choices=CATEGORY_CHOICES):
    """return all active listings under a category"""
    for (k,v) in choices:
        if v == category: 
            listings = Listing.objects.filter(category=k)

            return (category, listings)