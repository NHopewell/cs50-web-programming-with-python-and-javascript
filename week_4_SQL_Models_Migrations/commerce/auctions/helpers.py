import datetime

from .models import User, Listing, Watchlist, CATEGORY_CHOICES

def get_diff_days(date):

    date_format = "%Y-%m-%d"
    date_one = datetime.datetime.strptime(str(date).split()[0], date_format)
    date_two = datetime.datetime.strptime(str(datetime.date.today()), date_format)

    delta_days = (date_two - date_one).days

    return delta_days


def map_category(category, choices=CATEGORY_CHOICES):

   for (k,v) in choices:
       if k == category:
           return v

def all_categories(Listing):

    all_categories = ['Art & Collectibles', 'Clothing', 
        'Electronics', 'Health & Beauty', 'Home & Yard', 
        'Jewellery', 'Sporting Goods']

    category_listings = [Listing.objects.filter(category=cat) for cat in all_categories]

    categories = dict(zip(all_categories, category_listings))

    return categories

def get_listings_by_category(Listing, category, choices=CATEGORY_CHOICES):

    for (k,v) in choices:
        if v == category: 
            listings = Listing.objects.filter(category=k)

            return (category, listings)