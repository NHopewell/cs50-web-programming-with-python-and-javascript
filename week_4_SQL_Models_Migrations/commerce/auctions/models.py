from django.contrib.auth.models import AbstractUser
from django.db import models
from  django.utils import timezone


class User(AbstractUser):
    
    def __str__(self):
        return f"id: {self.id}, name: {self.first_name} {self.last_name}""


class Listing(models.Model):
    title = models.CharField(max_length=100)
    list_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(default='default.png', upload_to='listing_pics')
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, posted by: {self.owner}."


class Bid(models.Model):
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    bidder = models.ForeignKey(User, no_delete=models.CASCADE)
    bid_date = date_posted = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid: {self.bid}, Bidder: {self.bidder}"


class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.author} on post titled: '{self.listing.title}'."
