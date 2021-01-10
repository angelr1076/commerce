from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from datetime import datetime


# Categories
categories = [
    ('misc', 'misc'),
    ('computers', 'computers'),
    ('toys', 'toys'),
    ('pets', 'pets'),
    ('beauty', 'beauty'),
    ('video games', 'video games'),
    ('auto', 'auto'),
    ('clothing', 'clothing'),
]


ACTIVE_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    listing_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_owner")
    listing_title = models.CharField(max_length=100)
    listing_description = models.TextField(max_length=1200)
    listing_img = models.URLField(null=True, blank=True, max_length=250)
    created_on = models.DateTimeField(auto_now=True)
    starting_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=1.00)
    current_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)

    # From above categories list
    category = models.CharField(
        max_length=30, choices=categories, default='misc')
    # From active or inactive list
    closed_auction = models.CharField(
        max_length=10, choices=ACTIVE_CHOICES, default="No")

    class Meta:
        ordering = ['-created_on']

    # Redirect for comments and bids
    def get_absolute_url(self):
        return reverse('auctions:viewlisting', args=[str(self.id)])

    def __str__(self):
        return f"Title: {self.listing_title}, Price: ${self.starting_price}, Posted By: {self.listing_owner}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    bid_amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.user}'s bid on {self.listing} is {self.bid_amount}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.listing}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=1200, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.content}"
