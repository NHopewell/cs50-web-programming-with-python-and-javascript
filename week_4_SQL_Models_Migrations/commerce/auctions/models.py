from django.contrib.auth.models import AbstractUser
from django.db import models
from  django.utils import timezone

from PIL import Image


class User(AbstractUser):
    
    def __str__(self):
        return f"id: {self.id}, name: {self.first_name} {self.last_name}."

nums = '1 2 3 4 5 6 7'.split()

labs = ['Weapons', 'Armor', 
'Bags', 'Gems', 'Consumables & Potions', 
'Trade Goods', 'Magical Items']

CATEGORY_CHOICES = list(zip(nums, labs))


class Listing(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30, blank=True, choices=CATEGORY_CHOICES)
    image = models.ImageField(default='default.png', upload_to='listing_pics')
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    date_posted = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, default="active")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title}, posted by: {self.owner}."

    def save(self, *args, **kwargs):
        """override save() to resize img to save
           room on file system"""
        super().save(*args, **kwargs)

        # resive img if larger
        img = Image.open(f"./{self.image.url}")

        if img.height < 100 or img.width < 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img = img.convert("RGB")
            img.save(f"./{self.image.url}") # save to same path


class ClosedAuctions(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    date_closed = models.DateTimeField(default=timezone.now)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_date = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="all_bids")

    def __str__(self):
        return f"Bid: {self.bid}, Bidder: {self.bidder}"


class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.author} on post titled: '{self.listing.title}'."


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
